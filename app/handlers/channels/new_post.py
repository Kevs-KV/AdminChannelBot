import logging

from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes


async def new_post(m: Message):
    logging.info(f'Новая публикация в {m.chat.title}')


def setup(dp: Dispatcher):
    dp.register_channel_post_handler(new_post, content_types=ContentTypes.ANY)
