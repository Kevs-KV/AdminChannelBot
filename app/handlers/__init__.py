from aiogram import Dispatcher

from app.handlers import admins, private, errors, channels


def setup_all_handlers(dp: Dispatcher):
    for module in (channels, admins, private, errors):
        module.setup(dp)
