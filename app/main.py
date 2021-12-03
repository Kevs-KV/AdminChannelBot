import logging

from app.middlewares.i18n import I18nMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import start_polling
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app import handlers, middlewares, filters
from app.config import Config
from app.utils import logger
from app.utils.clear_dirs import clear_directories
from app.utils.db import MyODManticMongo
from app.utils.notifications.startup_notify import notify_superusers
from app.utils.set_bot_commands import set_commands


async def on_startup(dp):
    middlewares.setup(dp)
    filters.setup(dp)
    handlers.setup_all_handlers(dp)
    logger.setup_logger()

    clear_directories()

    mongo = MyODManticMongo()

    dp.bot["mongo"]: AsyncIOMotorClient = mongo
    dp.bot["db"]: MyODManticMongo = mongo.get_engine()
    dp.bot["scheduler"]: AsyncIOScheduler = AsyncIOScheduler()
    dp.bot["scheduler"].start()

    await notify_superusers(Config.ADMINS)
    await set_commands(dp)


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    if mongo := dp.bot.get('mongo', None):
        await mongo.close()
        await mongo.wait_closed()
    logging.warning("Bye!")


def main():
    bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MongoStorage(
        host=Config.MONGODB_HOSTNAME,
        port=Config.MONGODB_PORT,
        db_name=f"{Config.MONGODB_DATABASE}_fsm",
        password=Config.MONGODB_PASSWORD,
        uri=Config.MONGODB_URI,

    )
    dp = Dispatcher(bot, storage=storage)
    i18n = I18nMiddleware("bot", path=Config.LOCALES_PATH)
    bot["i18n"] = i18n
    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)