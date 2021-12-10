from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from aiogram.utils.exceptions import BotKicked
from odmantic import AIOEngine

from app.keyboards.inline import ChannelUserMarkup
from app.keyboards.reply import CancelUserAction
from app.middlewares import i18n
from app.models import UserModel
from app.states.bot_states import AddChannels
from app.utils.valid.valid_admins_channel import valid_admin_in_channels


async def add_channels(m: Message, _: i18n):
    await m.answer(_('Добавьте свой канал, (просто перешлите любую публикацию из вашего канала)'),
                   reply_markup=CancelUserAction().get(_))
    await AddChannels.user_channels.set()


async def add_channels_user(m: Message, db: AIOEngine, bot: Bot, user: UserModel, state: FSMContext, _: i18n):
    try:
        channel = m.forward_from_chat['id']
        admins_object = await bot.get_chat_administrators(chat_id=channel)
        admins_chat = [dict(admin.user) for admin in admins_object]
        user_id = m.from_user.id
        valid = await valid_admin_in_channels(m, admins_chat, user_id, _)
        if valid:
            if channel not in user.channels:
                await m.answer(_('Канал добавлен'))
                user.channels.append(channel)
                await db.save(user)
                await state.finish()
            else:
                await m.answer(_('Канал уже был дабавлен'))
                await state.finish()
        else:
            await m.answer(_('Вы не являетесь администратором канала'))
    except BotKicked:
        await m.answer(_('Бот не имеет доступа к каналу'))
        await state.finish()
    except TypeError:
        await m.answer(_('Перешлите публикацию из канала'))


async def user_channels(m: Message, user: UserModel, bot: Bot, _: i18n):
    markup = await ChannelUserMarkup(user, bot).get()
    await m.answer(_('Ваши каналы:'), reply_markup=markup)


def setup(dp: Dispatcher):
    dp.register_message_handler(add_channels, commands='add_channel')
    dp.register_message_handler(add_channels_user, state=AddChannels.user_channels, content_types=ContentTypes.ANY)
    dp.register_message_handler(user_channels, commands='my_channels')
