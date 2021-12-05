from aiogram import Dispatcher
from aiogram.types import Message

from app.middlewares import i18n


async def get_start_message(m: Message, _: i18n):
    await m.answer(_('Привет, данный бот предназначен для администрования телеграм каналов, '))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")
