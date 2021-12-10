from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.exceptions import BotKicked
from odmantic import AIOEngine

from app.keyboards.inline import ChoiceChannelForPost, ConfirmationMarkup
from app.keyboards.reply import CancelUserAction
from app.middlewares import i18n
from app.models import UserModel
from app.states.bot_states import PostChannelUser
from app.utils.scheduler.scheduler_jobs import scheduler_jobs, save_db_tasks, del_db_tasks
from app.utils.valid.valid_admins_channel import valid_time_posting


async def start_message_in_post(m: Message, _: i18n):
    await m.answer(_('Напишите текст для публикации'), reply_markup=CancelUserAction().get(_))
    await PostChannelUser.text.set()


async def add_text_post(m: Message, state: FSMContext, user: UserModel, bot: Bot, _: i18n):
    try:
        await state.update_data(message_id=m.message_id)
        await state.update_data(from_chat_id=m.chat.id)
        markup = await ChoiceChannelForPost(user, bot).get()
        await m.answer(_('Выберите канал для публикации'), reply_markup=markup)
        await PostChannelUser.channel.set()
    except BotKicked:
        await m.answer(_('У вас нет каналов, добавьте свой канал - /add_channel'))
        await state.finish()


async def add_channel_for_post(query: CallbackQuery, state: FSMContext, callback_data: dict, _: i18n):
    await state.update_data(channel_id=int(callback_data['value']))
    confirmation = await ConfirmationMarkup().get(_)
    await query.message.edit_text(_('Вы уверены?'), reply_markup=confirmation)
    await PostChannelUser.confirmation.set()


async def posting_in_channel(query: CallbackQuery, user: UserModel, bot: Bot, callback_data: dict, _: i18n):
    await query.message.edit_reply_markup()
    await query.message.delete()
    if callback_data["agreement"] == 'yes':
        await query.message.answer(_('Пришлите время постинга в формате Час/Минута/День/Мес/Год'),
                                   reply_markup=CancelUserAction().get(_))
        await PostChannelUser.data_time.set()
    else:
        markup = await ChoiceChannelForPost(user, bot).get()
        await query.message.answer(_('Выберите канал для публикации'), reply_markup=markup)
        await PostChannelUser.channel.set()


async def time_posting_in_channel(m: Message, bot: Bot, state: FSMContext, db: AIOEngine, user: UserModel, _: i18n):
    try:
        data_time = [int(data) for data in m.text.split('/')]
        result = await state.get_data()
        channel_id = result.get('channel_id')
        await state.finish()
        user_id = m.from_user.id
        post = user.posts + 1
        id_task = f'{user_id}-{post}'
        message_id = result.get('message_id')
        from_chat_id = result.get('from_chat_id')
        await valid_time_posting(user, data_time)
        await save_db_tasks(bot, db, user, message_id, from_chat_id, data_time, channel_id, id_task)
        await m.answer(_('Задача добавлена'), reply_markup=ReplyKeyboardRemove())
        return scheduler_jobs(db, user, _, message_id, from_chat_id, bot, channel_id, data_time, id_task)
    except BotKicked:
        await m.answer(_('Бот не имеет доступа к каналу'))
        await state.finish()
    except ValueError:
        await m.answer(_('Вы ввели неправильную дату'))
        await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(start_message_in_post, commands='post')
    dp.register_message_handler(add_text_post, state=PostChannelUser.text, content_types=types.ContentType.ANY)
    dp.register_callback_query_handler(add_channel_for_post, ChoiceChannelForPost.callback_data.filter(),
                                       state=PostChannelUser.channel)
    dp.register_callback_query_handler(posting_in_channel, ConfirmationMarkup.callback_data.filter(),
                                       state=PostChannelUser.confirmation)
    dp.register_message_handler(time_posting_in_channel, state=PostChannelUser.data_time)
