import functools

from aiogram import Dispatcher
from aiogram.types import Message


async def get_start_message(m: Message, t: functools.partial):
    await m.answer(t("locale.start"))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")
