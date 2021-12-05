from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from odmantic import AIOEngine

from app.keyboards.inline import ChoiceChannelForPost, ConfirmationMarkup
from app.middlewares import i18n
from app.models import UserModel
from app.states.bot_states import PostChannelUser
from app.utils.scheduler.scheduler_jobs import scheduler_jobs, save_db_tasks


async def start_message_in_post(m: Message, _: i18n):
    await m.answer(_('Напишите текст для публикации'))
    await PostChannelUser.text.set()


async def add_text_post(m: Message, state: FSMContext, user: UserModel, bot: Bot, _: i18n):
    await state.update_data(message_id=m.message_id)
    await state.update_data(from_chat_id=m.chat.id)
    markup = await ChoiceChannelForPost(user, bot).get()
    await m.answer(_('Выберите канал для публикации'), reply_markup=markup)
    await PostChannelUser.channel.set()


async def add_channel_for_post(query: CallbackQuery, state: FSMContext, callback_data: dict, _: i18n):
    await query.message.edit_reply_markup()
    await query.message.delete()
    await state.update_data(channel_id=int(callback_data['value']))
    confirmation = await ConfirmationMarkup().get()
    await query.message.answer(_('Вы уверены?'), reply_markup=confirmation)
    await PostChannelUser.confirmation.set()


async def posting_in_channel(query: CallbackQuery, _: i18n):
    await query.message.edit_reply_markup()
    await query.message.delete()
    await query.message.answer(_('Пришлите время постинга в формате Час/Минута/День/Мес/Год'))
    await PostChannelUser.data_time.set()


async def time_posting_in_channel(m: Message, bot: Bot, state: FSMContext, db: AIOEngine, user: UserModel, _: i18n):
    data_time = [int(data) for data in m.text.split('/')]
    result = await state.get_data()
    channel_id = result.get('channel_id')
    await m.answer(_('Готово'))
    await state.finish()
    user_id = m.from_user.id
    post = user.posts + 1
    id_tasks = f'{user_id}-{post}'
    message_id = result.get('message_id')
    from_chat_id = result.get('from_chat_id')
    await save_db_tasks(bot, db, user, message_id, from_chat_id, data_time, channel_id, id_tasks)
    return scheduler_jobs(db, user, message_id, from_chat_id, bot, channel_id, data_time, id_tasks)


def setup(dp: Dispatcher):
    dp.register_message_handler(start_message_in_post, commands='post')
    dp.register_message_handler(add_text_post, state=PostChannelUser.text, content_types=types.ContentType.ANY)
    dp.register_callback_query_handler(add_channel_for_post, ChoiceChannelForPost.callback_data.filter(),
                                       state=PostChannelUser.channel)
    dp.register_callback_query_handler(posting_in_channel, ConfirmationMarkup.callback_data.filter(),
                                       state=PostChannelUser.confirmation)
    dp.register_message_handler(time_posting_in_channel, state=PostChannelUser.data_time)
