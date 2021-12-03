from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from odmantic import AIOEngine

from app.keyboards.inline import ChannelUserMarkup
from app.models import UserModel
from app.states.bot_states import AddChannels
from app.utils.valid.valid_admins_channel import valid_admin_in_channels

scheduler = AsyncIOScheduler()


async def start_bot(m: Message, bot: Bot):
    await m.answer('Привет')


async def add_channels(m: Message, bot: Bot):
    await m.answer('Добавьте своего бота')
    await AddChannels.user_channels.set()


async def add_channels_user(m: Message, db: AIOEngine, bot: Bot, user: UserModel, state: FSMContext):
    try:
        channel = m.forward_from_chat['id']
        admins_object = await bot.get_chat_administrators(chat_id=channel)
        admins_chat = [dict(admin.user) for admin in admins_object]
        user_id = m.from_user.id
        valid = await valid_admin_in_channels(m, admins_chat, user_id)
        if valid:
            await m.answer('Проверка пройдена')
            user_chanels = user.channels
            user_chanels.append(channel)
            user.channels = user_chanels
            await db.save(user)
        else:
            await m.answer('Проверка не пройдена')
    except:
        await m.answer('Бот не имеет доступа к каналу')
        await state.finish()


async def user_channels(m: Message, user: UserModel, bot: Bot):
    user_channels = user.channels
    print(user_channels)
    mark = await ChannelUserMarkup(user, bot).get()
    await m.answer(f'Ваши каналы:', reply_markup=mark)
    # for channel in user_channels:
    #     print(channel_info)
    #     await m.answer(f'<a href="{channel_info["invite_link"]}">{channel_info["title"]}</a>')


def setup(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start')
    dp.register_message_handler(add_channels, commands='add_bot')
    dp.register_message_handler(add_channels_user, state=AddChannels.user_channels, content_types=ContentTypes.ANY)
    dp.register_message_handler(user_channels, commands='my_channels')
