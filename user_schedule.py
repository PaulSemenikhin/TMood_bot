import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import asyncio
from config_data.config import Config, load_config
import logging
from database import db_functions

# Загружаем конфиг в переменную config
config: Config = load_config()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token)

scheduler = AsyncIOScheduler()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def periodic_task():
    while True:
        await asyncio.sleep(3600)


async def delete_notification(user_id):
    for job in scheduler.get_jobs():
        if job.id == str(user_id):
            scheduler.remove_job(job.id)
            logger.info(f"Удалена работа {job.id}, Все работы: {scheduler.get_jobs()}")


async def update_notification(user_id, time_str):
    hour, minute = map(int, time_str.split(':'))
    print(f'Работы - {scheduler.get_jobs()}')
    for job in scheduler.get_jobs():
        print(job.id, user_id)
        if job.id == str(user_id):
            logger.info(f"Found matching job ID: {job.id}, Next run time: {job.next_run_time}")
            scheduler.remove_job(job.id)
            scheduler.add_job(notify_user, 'cron', args=[user_id], id=f'{user_id}', hour=hour, minute=minute)
            logger.info(f"Job ID {job.id} rescheduled for {time_str}")
            return job.next_run_time


async def notify_user(user_id, message_text='Как прошел ваш день?'):
    await bot.send_message(user_id, message_text)


async def main():

    users = await db_functions.get_time_notify_not_null()

    for user_id, time_notify in users:
        print(f"User ID: {user_id}, Time: {time_notify}")
        hour, minute = map(int, time_notify.split(':'))
        scheduler.add_job(notify_user, 'cron', args=[user_id], id=f'{user_id}', hour=hour, minute=minute)

    scheduler.start()
    for job in scheduler.get_jobs():
        print(job.id)


if __name__ == '__main__':
    asyncio.create_task(periodic_task())
    asyncio.run(main())
