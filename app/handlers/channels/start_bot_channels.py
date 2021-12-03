from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from odmantic import AIOEngine

from app.keyboards.inline import ChannelUserMarkup
from app.middlewares import i18n
from app.models import UserModel
from app.states.bot_states import AddChannels
from app.utils.valid.valid_admins_channel import valid_admin_in_channels


async def add_channels(m: Message, _: i18n):
    await m.answer(_('Добавьте своего бота'))
    await AddChannels.user_channels.set()


async def add_channels_user(m: Message, db: AIOEngine, bot: Bot, user: UserModel, state: FSMContext, _: i18n):
    try:
        channel = m.forward_from_chat['id']
        admins_object = await bot.get_chat_administrators(chat_id=channel)
        admins_chat = [dict(admin.user) for admin in admins_object]
        user_id = m.from_user.id
        valid = await valid_admin_in_channels(m, admins_chat, user_id, _)
        if valid:
            await m.answer(_('Проверка пройдена'))
            user.channels.append(channel)
            await db.save(user)
        else:
            await m.answer(_('Проверка не пройдена'))
    except:
        await m.answer(_('Бот не имеет доступа к каналу'))
        await state.finish()


async def user_channels(m: Message, user: UserModel, bot: Bot, _: i18n):
    markup = await ChannelUserMarkup(user, bot).get()
    await m.answer(_('Ваши каналы:'), reply_markup=markup)


def setup(dp: Dispatcher):
    dp.register_message_handler(add_channels, commands='add_bot')
    dp.register_message_handler(add_channels_user, state=AddChannels.user_channels, content_types=ContentTypes.ANY)
    dp.register_message_handler(user_channels, commands='my_channels')
