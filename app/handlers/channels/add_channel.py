from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from aiogram.utils.exceptions import BotKicked, ChatAdminRequired
from odmantic import AIOEngine

from app.keyboards.inline import ChannelUserMarkup
from app.keyboards.reply import CancelUserAction
from app.middlewares import i18n
from app.models import UserModel
from app.states.bot_states import AddChannels
from app.utils.valid.valid_admins_channel import valid_admin_in_channels


async def add_channel(m: Message, _: i18n):
    await m.answer(_('Добавьте свой канал, (просто перешлите любую публикацию из вашего канала)'),
                   reply_markup=CancelUserAction().get(_))
    await AddChannels.user_channels.set()


async def add_channel_user(m: Message, db: AIOEngine, bot: Bot, user: UserModel, state: FSMContext, _: i18n):
    try:
        channel = m.forward_from_chat['id']
        admins_object = await bot.get_chat_administrators(chat_id=channel)
        admins_chat = [dict(admin.user) for admin in admins_object]
        user_id = m.from_user.id
        valid = await valid_admin_in_channels(m, admins_chat, user_id, _)
        if valid:
            if channel not in user.channels:
                await m.answer(_('Канал добавлен'), reply_markup=ReplyKeyboardRemove())
                user.channels.append(channel)
                await db.save(user)
                await state.finish()
            else:
                await m.answer(_('Канал уже был дабавлен'), reply_markup=ReplyKeyboardRemove())
                await state.finish()
        else:
            await m.answer(_('Вы не являетесь администратором канала'), reply_markup=ReplyKeyboardRemove())
    except (BotKicked, ChatAdminRequired):
        await m.answer(_('Бот не имеет доступа к каналу'), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    except TypeError:
        await m.answer(_('Перешлите публикацию из канала'), reply_markup=ReplyKeyboardRemove())


async def user_channel(m: Message, user: UserModel, bot: Bot, _: i18n):
    markup = await ChannelUserMarkup(user, bot).get()
    await m.answer(_('Ваши каналы:'), reply_markup=markup)


def setup(dp: Dispatcher):
    dp.register_message_handler(add_channel, commands='add_channel')
    dp.register_message_handler(add_channel_user, state=AddChannels.user_channels, content_types=ContentTypes.ANY)
    dp.register_message_handler(user_channel, commands='my_channels')
