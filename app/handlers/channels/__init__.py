from aiogram import Dispatcher

from app.handlers.channels import new_post, start_bot_channels, poster, scheduler_control


def setup(dp: Dispatcher):
    for module in (new_post, start_bot_channels, poster, scheduler_control):
        module.setup(dp)
