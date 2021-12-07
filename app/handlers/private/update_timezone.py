from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from odmantic import AIOEngine

from app.middlewares import i18n
from app.models import UserModel
from app.states.timezone_states import TimezoneUser


async def update_timezone(m: Message):
    await m.answer('Введите часовой пояс в формате UTC (прим: +3)')
    await TimezoneUser.timezone.set()


async def save_timezone_user(m: Message, state: FSMContext, user: UserModel, db: AIOEngine, _: i18n):
    try:
        zone = user.timezone
        if 0 <= int(m.text) <= 11:
            zone = f'-{int(m.text)}'
        elif 0 > int(m.text) >= -11:
            zone = f'+{int(m.text[1::])}'
        else:
            await state.finish()
            return await m.answer(_('Некорректные данные'))
        user.timezone = f'Etc/GMT{zone}'
        await db.save(user)
        await m.answer(_('Часовой пояс установлен'))
        await state.finish()
    except ValueError:
        await m.answer(_('Некорректные данные'))
        await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(update_timezone, commands='timezone')
    dp.register_message_handler(save_timezone_user, state=TimezoneUser.timezone)
