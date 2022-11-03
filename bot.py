import asyncio
import logging
from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from handlers.stock import register_handlers_stock
from handlers.common import register_handlers_common, register_callbacks_handler
from database.sqlite import db_start_stock


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description=f"Запуск/перезапуск бота"),
        BotCommand(command="/list_of_commands", description=f"Список команд"),
        BotCommand(command="/ny_stock_2023", description="Активировать дивиденды"),
        BotCommand(command="/help", description='Проблемы с ботом? Жми сюда'),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    config = load_config("config/bot.ini")
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp, config.tg_bot.admin_id)
    register_handlers_stock(dp)
    register_callbacks_handler(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск БД
    await db_start_stock()

    # Запуск поллинга
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
