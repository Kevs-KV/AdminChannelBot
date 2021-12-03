from aiogram import Dispatcher, Bot
from aiogram.types import Message, ChatMemberOwner, ContentTypes


async def new_post(m: Message, bot: Bot):
    print(f'{m.chat}')
    print(f'Новая публикация в {m.chat.title}')
    admins_object = await bot.get_chat_administrators(chat_id=m.chat.id)
    admins_chat = [dict(admin.user) for admin in admins_object]
    print(f'{admins_chat}')



def setup(dp: Dispatcher):
    dp.register_channel_post_handler(new_post, content_types=ContentTypes.ANY)
