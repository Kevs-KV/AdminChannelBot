from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def user_commands_cancel(m: Message, state: FSMContext):
    await state.finish()