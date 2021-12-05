from aiogram import Dispatcher

from app.handlers.private import default, start, update_language, help_


def setup(dp: Dispatcher):
    for module in (start, update_language, default, help_):
        module.setup(dp)
