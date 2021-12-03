from datetime import datetime

from aiogram import Bot
from odmantic import AIOEngine

from app.models import UserModel


async def send_message_channels(bot: Bot, user: UserModel, message_id, from_chat_id, db: AIOEngine, channel_id,
                                id_tasks):
    await bot.copy_message(chat_id=channel_id, message_id=message_id, from_chat_id=from_chat_id)
    del user.tasks[id_tasks]
    await db.save(user)


async def save_db_tasks(bot: Bot, db: AIOEngine, user: UserModel, message_id, from_chat_id, data_time, channel_id,
                        id_tasks):

    channel_info = await bot.get_chat(chat_id=channel_id)
    title_channel = channel_info['title']
    user.tasks.update({id_tasks: [title_channel, channel_id, message_id, from_chat_id, data_time]})
    await db.save(user)


async def del_db_tasks(user: UserModel, db: AIOEngine, id_task):
    del user.tasks[id_task]
    await db.save(user)


async def changing_task_time(bot: Bot, db: AIOEngine, user: UserModel, id_tasks, data_time):
    print(user.tasks)
    print(user.tasks[id_tasks][:-1:])
    title_channel, channel_id, message_id, from_chat_id = user.tasks[id_tasks][:-1:]
    await del_db_tasks(user, db, id_tasks)
    await save_db_tasks(bot, db, user, message_id, from_chat_id, data_time, channel_id, id_tasks)
    bot['scheduler'].remove_job(id_tasks)
    return scheduler_jobs(db, user, message_id, from_chat_id, bot, channel_id, data_time, id_tasks)



def scheduler_jobs(db: AIOEngine, user: UserModel, message_id, from_chat_id, bot, channel_id, data_time, id_tasks):
    hour, minute, day, month, year = data_time
    bot['scheduler'].add_job(send_message_channels, "date", run_date=datetime(year, month, day, hour, minute),
                             args=(bot, user, message_id, from_chat_id, db, channel_id, id_tasks), id=id_tasks)
