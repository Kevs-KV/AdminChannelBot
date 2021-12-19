from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import quote_html

from app.middlewares import i18n
from app.models import UserModel


async def get_default_message(m: Message, _: i18n):
    await m.answer(_('Нет такой команды, cписок команд - /help'))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_default_message)
