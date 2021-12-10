from datetime import datetime

from aiogram import Bot
from aiogram.types import Message
from odmantic import AIOEngine
from pytz import timezone

from app.middlewares import i18n
from app.models import UserModel


async def valid_admin_in_channels(m: Message, admins_chat, user_id, _: i18n):
    for admin in admins_chat:
        if admin['id'] == user_id:
            return True
    else:
        await m.answer(_('Вы не администратор канала'))
        return False


async def valid_time_posting(bot: Bot, user: UserModel, db: AIOEngine, data_time):
    hour, minute, day, month, year = data_time
    user_timezone = timezone(user.timezone)
    if datetime.now(user_timezone) < user_timezone.localize(datetime(year, month, day, hour, minute)):
        return True
    raise ValueError

