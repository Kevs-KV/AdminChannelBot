from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.middlewares import i18n


async def user_command_cancel_state(m: Message, state: FSMContext, _: i18n):
    await state.finish()
    await m.answer(_('Отменено'))


def setup(dp: Dispatcher):
    dp.register_message_handler(user_command_cancel_state, state='*')
