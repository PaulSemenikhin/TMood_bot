import sqlite3
import os


# Функция инициализации ДБ
def init_db():
    db_path = 'data.db'
    db_exists = os.path.exists(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if not db_exists:
        # SQL-запрос на создание таблицы "users"
        cur.execute('CREATE TABLE IF NOT EXISTS users ('
                    'user_id INTEGER UNIQUE, '
                    'date_start_bot DATE, '
                    'time_notify TIME, '
                    'depression_notification INTEGER DEFAULT 0, '
                    'depression_time DATE)')

        # SQL-запрос на создание таблицы "moods"
        cur.execute('CREATE TABLE IF NOT EXISTS moods ('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'user_id INTEGER, '
                    'date DATETIME, '
                    'mood_value INTEGER, '
                    'other_field TEXT, '
                    'FOREIGN KEY (user_id) REFERENCES users (user_id) ON '
                    'DELETE CASCADE)')

        conn.commit()

    conn.close()

# TODO: протестировать создание ДБ
