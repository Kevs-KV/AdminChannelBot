from aiogram import Dispatcher
from aiogram.types import Message


async def get_help_message(m: Message):
    text = ('Список команд:',
            '/start - запустить бота',
            '/post - создать задачу для постинга',
            '/help - получить справку',
            '/add_channel - добавить канал',
            '/view_task - посмотреть задачи',
            '/action_task - работа с задачей',
            '/update_language - изменить язык',
            '/timezone - изменить часовой пояс',
            '/my_channels - посмотреть список каналов')

    await m.answer("\n".join(text))


async def get_help_message_admin(m: Message):
    text = ('Список команд:',
            'Количество пользователей в базе данных - /amount',
            'Количество активных пользователей - /exists_amount',
            'Запись пользователей в файл - /users_file',
            'Отмена - /cancel_all')

    await m.answer("\n".join(text))


def setup(dp: Dispatcher):
    dp.register_message_handler(get_help_message, commands="help")
    dp.register_message_handler(get_help_message_admin, commands='help_admin', is_admin=True)
