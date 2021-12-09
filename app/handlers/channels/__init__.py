from aiogram import Dispatcher

from app.handlers.channels import cancel, new_post, start_bot_channels, poster, scheduler_control


def setup(dp: Dispatcher):
    for module in (cancel, new_post, start_bot_channels, poster, scheduler_control):
        module.setup(dp)
