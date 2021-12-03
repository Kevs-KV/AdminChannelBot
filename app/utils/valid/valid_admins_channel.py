from aiogram.contrib.middlewares import i18n
from aiogram.types import Message


async def valid_admin_in_channels(m: Message, admins_chat, user_id, _: i18n):
    for admin in admins_chat:
        if admin['id'] == user_id:
            return True
    else:
        await m.answer('Вы не администратор канала')
        return False


