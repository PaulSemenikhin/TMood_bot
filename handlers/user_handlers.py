import datetime
import io
import logging
import re

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sqlalchemy import create_engine, text

from aiogram import Bot, Router, types
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove

import user_schedule
from keyboards import keyboards
from database import db_functions
from lexicon.lexicon import LEXICON


router: Router = Router()


# Хэндлер, срабатывающий на команду "/start" -
# добавляет пользователя в БД, если его там еще не было
# и отправляет ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'])
    user_id = message.from_user.id  # type: ignore
    if not await db_functions.check_user_exists(user_id):
        await db_functions.add_new_user(user_id)
    await message.answer(LEXICON['start_settings_button'],
                         reply_markup=keyboards.start_choice)


# Хэндлер, срабатывающий на команду "/help" -
# отправляет пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
@router.message(Text(text='🛟Помощь'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


# Хэндлер, срабатывающий на команду "/settime" и текст "Да😊" или "⏰Время уведомлений" -
# отправляет сообщение с кнопками выбора времени уведомлений
@router.message(Text(text='Да😊'))
@router.message(Command(commands='settime'))
@router.message(Text(text='⏰Время уведомлений'))
async def process_setting_command_yes(message: Message):
    await message.answer(LEXICON['reminderset'], reply_markup=keyboards.kb_builder_time.as_markup(
                                            resize_keyboard=True))


# Хэндлер, срабатывающий на текст "Нет😒" -
# убирает клавиатуру и отправляет сообщение об отказе от выбора
@router.message(Text(text='Нет😒'))
async def process_setting_command_no(message: Message):
    await message.answer(LEXICON['no_choice'],
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))


# Хэндлер, срабатывающий на сообщения, содержащие время в формате HH:MM -
# обновляет время уведомлений в БД и планировщике
@router.message(lambda message: re.match(r"\d{1,2}:\d{2}", message.text))
async def process_time_message(message: Message):
    logger = logging.getLogger(__name__)

    time_str = message.text.strip()  # type: ignore

    user_id = message.from_user.id  # type: ignore

    try:

        # Log received user ID and time
        logger.info(f"Updating time notification for user ID: {user_id}, New time: {time_str}")

        await db_functions.update_time_notify(user_id, time_str)

        # Log successful database update
        logger.info(f"Time notification updated for user ID: {user_id}")

        await user_schedule.update_notification(user_id, time_str)

        await message.answer(LEXICON['setdone'], reply_markup=keyboards.defualt_kb)

    except ValueError:
        await message.answer('Неправильный формат времени.'
                             '\nПожалуйста, введите время в формате HH:MM.')


# Хэндлер, срабатывающий на команду "/deletenotification" и текст "🚫Убрать напоминания" -
# удаляет уведомления для пользователя
@router.message(Command(commands='deletenotification'))
@router.message(Text(text='🚫Убрать напоминания'))
async def process_deletion_notification(message: Message):
    user_id = message.from_user.id  # type: ignore
    await user_schedule.delete_notification(user_id)
    await message.answer('Я больше не буду напоминать внести запись о настроении😞')


# Хэндлер, срабатывающий на команду "/mood" и текст "📝Внести запись" -
# отправляет сообщение с кнопками для записи настроения
@router.message(Command(commands='mood'))
@router.message(Text(text='📝Внести запись'))
async def process_write_record(message: Message):
    await message.answer(LEXICON['today_mood'], reply_markup=keyboards.kb_builder_mood.as_markup(
                                            resize_keyboard=True))


# Хэндлер, срабатывающий на сообщения с оценкой настроения (1-10) -
# добавляет запись настроения в БД и проверяет уровень депрессии
@router.message(lambda message: message.text.isdigit() and 1 <= int(message.text) <= 10)
async def process_mood_score(message: Message):
    mood_score = int(message.text)  # type: ignore
    user_id = message.from_user.id  # type: ignore
    current_date = datetime.datetime.now().date()

    try:
        await db_functions.add_mood_score(user_id, mood_score)
        print(await db_functions.process_depression_test(user_id))
        await message.answer("Запись о настроении успешно добавлена!",
                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

        first_launch_time = await db_functions.get_first_launch_time(user_id)
        days_since_first_launch = current_date - first_launch_time

        # Проверяем, было ли уже отправлено сообщение о депрессии
        if await db_functions.depression_notification(user_id):
            last_depression_time = datetime.datetime.strptime(
                    await db_functions.get_time_depression(user_id),
                    "%Y-%m-%d"
                ).date()
            days_since_last_depression = current_date - last_depression_time
            # Если прошло менее 7 дней с момента запуска бота, то далее не обрабатываем
            if days_since_first_launch.days < 7:
                return

            # Если прошло более 14 дней с момента первого сообщения о депрессии
            if days_since_last_depression >= datetime.timedelta(days=14):
                # Проверяем среднее настроение за последние 14 дней
                if await db_functions.process_depression_test(user_id) < 5.0:
                    # Отправляем повторное сообщение о депрессии
                    await db_functions.set_time_depression(user_id)
                    await message.answer(LEXICON['repeat_depression'])
                else:
                    # Сбрасываем уведомление о депрессии
                    await db_functions.set_depression_notification(user_id, 0)
            else:
                # Прошло менее 14 дней, пропускаем проверку
                pass

        # Если среднее настроение меньше 5 и уведомление о депрессии еще не отправлялось
        elif await db_functions.process_depression_test(user_id) < 5.0:
            await db_functions.set_time_depression(user_id)
            await db_functions.set_depression_notification(user_id, 1)
            await message.answer(LEXICON['depression_detected'])

    except Exception as e:
        await message.answer('Произошла ошибка при добавлении '
                             'записи о настроении.')
        print(f"Ошибка при добавлении записи о настроении: {e}")


# Хэндлер, срабатывающий на команду "/delete" и текст "❌Удалить запись" -
# удаляет последнюю запись настроения пользователя
@router.message(Command(commands='delete'))
@router.message(Text(text='❌Удалить запись'))
async def process_delete_last_record(message: Message):
    try:
        await db_functions.delete_last_record(message.from_user.id)  # type: ignore
        await message.answer(LEXICON['entry_deleted'])
    except Exception as e:
        await message.answer('Произошла ошибка при удалении '
                             'записи о настроении.')
        print(f"Ошибка при удалении записи о настроении: {e}")


# Хэндлер, срабатывающий на команду "/chart" и текст "📈График настроения" -
# генерирует и отправляет пользователю график настроения за последние 30 дней
@router.message(Command(commands='chart'))
@router.message(Text(text='📈График настроения'))
async def get_chart(message: Message, bot: Bot):

    engine = create_engine("sqlite:///data.db")

    # Загрузка данных
    query = text("SELECT * FROM moods WHERE user_id = :user_id")
    df = pd.read_sql_query(query, engine, params={"user_id": message.chat.id})

    # Конвертация даты
    df['date'] = pd.to_datetime(df['date'])

    # Фильтрация данных за последние 30 дней
    end_date = df['date'].max()
    start_date = end_date - pd.Timedelta(days=29)
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Создание графика
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="date", y="mood_value", data=df_filtered, ax=ax)

    # Настройка графика
    ax.set_xlabel("Дата", fontsize=14)
    ax.set_ylabel("Настроение", fontsize=14)
    ax.set_title("Ваш график настроения за последние 30 дней", fontsize=16)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Сохранение графика (можно также отправить его напрямую, без сохранения)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    photo_file = types.BufferedInputFile(buffer.getvalue(), filename='my_chart.png')

    await bot.send_photo(message.chat.id, photo=photo_file, caption="Ваш график настроения за последние 30 дней")
