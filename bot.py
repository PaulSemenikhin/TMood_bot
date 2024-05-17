import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards import main_menu
import user_schedule
from database.database import init_db


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - :%(funcName)s - %(name)s - %(message)s')

    logger.info('Starting bot')

    # Загружаем конфигурационные данные
    config: Config = load_config()

    # Инициализируем базу данных
    init_db()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Настраиваем главное меню бота
    await main_menu.set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Запускаем расписание уведомлений
    await user_schedule.main()

    await dp.start_polling(bot)

    await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
