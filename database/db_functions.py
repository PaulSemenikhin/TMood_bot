import sqlite3
import datetime
import aiosqlite


# Инициализируем соединение с БД
conn = sqlite3.connect('data.db')
cur = conn.cursor()
# TODO оно же уже не нужно?


# Выполняет произвольный SQL-запрос и возвращает результат
async def execute_query(query, *args):
    async with aiosqlite.connect('data.db') as db:
        async with db.execute(query, args) as cursor:
            return await cursor.fetchall()


# Выполняет SQL-запрос, который модифицирует данные в БД
async def execute_modify_query(query, *args):
    async with aiosqlite.connect('data.db') as db:
        async with db.execute(query, args):
            await db.commit()


# Проверяет, существует ли пользователь в БД по его user_id
async def check_user_exists(user_id):
    sql_query = '''
    SELECT * FROM users WHERE user_id = ?'''

    async with aiosqlite.connect('data.db') as db:
        async with db.execute(sql_query, (user_id,)) as cursor:
            existing_user = await cursor.fetchone()

    if existing_user:
        return True
    return False


# Добавляет нового пользователя в БД
async def add_new_user(user_id):
    current_date = datetime.datetime.now().date()
    # TODO при переносе в итоовую ДБ надо изменить порядок автозаполнения
    # так как я менял порядок в database для создания новой дб
    sql_query = '''
    INSERT INTO users VALUES(?, "0", NULL, NULL, "0", "0", ?)
    '''
    await execute_modify_query(sql_query, user_id, current_date)


# Обновляет время уведомления пользователя
async def update_time_notify(user_id, time_str):
    sql_query = '''
    UPDATE users SET time_notify = ? WHERE user_id = ?
    '''

    await execute_modify_query(sql_query, time_str, user_id)


# Получает дату первого запуска бота пользователем
async def get_first_launch_time(user_id):
    sql_query = '''
    SELECT date_start_bot FROM users WHERE user_id = ?
    '''
    result = await execute_query(sql_query, user_id)
    return datetime.date.fromisoformat(result[0][0])  # type: ignore


# Добавляет запись о настроении пользователя в БД
async def add_mood_score(user_id, mood_value, other_field=None):
    # Получаем текущую дату и время
    current_datetime = datetime.datetime.now()

    # Подготовленный SQL-запрос для добавления записи о настроении
    sql_query = '''
    INSERT INTO moods (user_id, date, mood_value, other_field)
    VALUES (?, ?, ?, ?)
    '''

    try:
        await execute_modify_query(sql_query, user_id, current_datetime.date(), mood_value, other_field)
        print("Запись о настроении успешно добавлена!")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при добавлении записи о настроении: {e}")


#
async def delete_last_record(user_id):
    sql_query = '''
    DELETE FROM moods
    WHERE id = (SELECT max(id)
                FROM moods
                WHERE user_id = ?)
    '''

    try:
        await execute_modify_query(sql_query, user_id)
        print("Запись о настроении успешно удалена!")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при удалении записи о настроении: {e}")

# TODO: нужны ли эти принты в try? скорре нет, убрать


# Вычисляет среднее настроение пользователя за последние 14 дней
async def process_depression_test(user_id):
    sql_query = '''
    SELECT AVG(mood)
    FROM (
        SELECT mood_value AS mood
        FROM moods
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 14
    ) AS recent_moods;
    '''

    result = await execute_query(sql_query, user_id)
    return result[0][0]  # type: ignore


# Проверяет, включены ли у пользователя уведомления о депрессии
async def depression_notification(user_id):
    sql_query = '''
    SELECT depression_notification
    FROM users
    WHERE user_id = ?
    '''
    result = await execute_query(sql_query, user_id)
    return result[0][0]  # type: ignore


# Включает или выключает уведомления о депрессии для пользователя
async def set_depression_notification(user_id, notification_value):
    sql_query = '''
    UPDATE users
    SET depression_notification = ?
    WHERE user_id = ?
    '''
    await execute_modify_query(sql_query, notification_value, user_id)


# Записывает текущую дату как последнее время проверки депрессии пользователя
async def set_time_depression(user_id):
    current_datetime = datetime.datetime.now()
    depression_date = current_datetime.date()

    sql_query = '''
    UPDATE users
    SET depression_time = ?
    WHERE user_id = ?
    '''

    await execute_modify_query(sql_query, depression_date, user_id)


# Получает последнее время проверки депрессии пользователя
async def get_time_depression(user_id):
    sql_query = '''
    SELECT depression_time
    FROM users
    WHERE user_id = ?
    '''

    result = await execute_query(sql_query, user_id)
    return result[0][0]  # type: ignore


# Получает список пользователей, у которых есть напоминания о предстоящих уведомлениях о депрессии
async def get_time_notify_not_null():
    sql_query = '''
    SELECT user_id, time_notify FROM users WHERE time_notify NOT NULL
    '''

    result = await execute_query(sql_query)
    return result
