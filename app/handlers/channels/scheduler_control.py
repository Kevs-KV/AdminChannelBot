from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageTextIsEmpty
from odmantic import AIOEngine

from app.keyboards.inline import TaskChannelMarkup
from app.keyboards.reply import ActionTaskChannel
from app.middlewares import i18n
from app.models import UserModel
from app.states.bot_states import ActionForTask
from app.utils.scheduler.scheduler_jobs import changing_task_time, del_db_tasks


async def get_list_posting(m: Message, user: UserModel, _: i18n):
    try:
        list_posting = []
        for task in user.tasks:
            title = user.tasks[task][0]
            hour, minute, day, month, year = user.tasks[task][-1]
            list_posting.append(_('Канал: {} дата: {}/{}/{} в {}:{}').format(title, day, month, year, hour, minute))
        await m.answer("\n".join(list_posting))
    except MessageTextIsEmpty:
        await m.answer(_('Нет задач'))


async def scheduler_jobs_list(m: Message, user: UserModel, bot: Bot, _: i18n):
    list_task = await TaskChannelMarkup(user, bot).get(_)
    await m.answer(_('Список задач в палировщике'), reply_markup=list_task)


async def view_post(query: CallbackQuery, user: UserModel, state: FSMContext, bot: Bot, _: i18n, callback_data: dict):
    await query.message.edit_reply_markup()
    task_id = callback_data['value']
    task = user.tasks[callback_data['value']]
    await state.update_data(task_id=task_id)
    title_channel, channel_id, message_id, from_chat_id, data_time = task
    markup = ActionTaskChannel().get(_)
    await bot.copy_message(chat_id=from_chat_id, message_id=message_id, from_chat_id=from_chat_id)
    await query.message.answer(_('Выберите  действие'), reply_markup=markup)
    await ActionForTask.action.set()


async def action_channel(m: Message, user: UserModel, state: FSMContext, db: AIOEngine, _: i18n):
    action = m.text
    if action == _('Отмена'):
        await m.answer(_('Отменено'), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif action == _('Изменить время'):
        await m.answer(_('Пришлите время постинга в формате Час/Минута/День/Мес/Год'),
                       reply_markup=ReplyKeyboardRemove())
        await ActionForTask.data_time.set()
    elif action == _("Удалить"):
        result = await state.get_data()
        task_id = result.get('task_id')
        await del_db_tasks(user, db, task_id)
        await m.answer(_('Задача отменена'), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await m.answer(_('Нет такой команды'))


async def new_time_for_post(m: Message, bot: Bot, user: UserModel, state: FSMContext, db: AIOEngine, _: i18n):
    data_time = [int(data) for data in m.text.split('/')]
    result = await state.get_data()
    task_id = result.get('task_id')
    await changing_task_time(bot, db, _, user, task_id, data_time)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(get_list_posting, commands='view_task')
    dp.register_message_handler(scheduler_jobs_list, commands='action_task')
    dp.register_callback_query_handler(view_post, TaskChannelMarkup.callback_data.filter())
    dp.register_message_handler(action_channel, state=ActionForTask.action)
    dp.register_message_handler(new_time_for_post, state=ActionForTask.data_time)
