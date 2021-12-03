from aiogram.dispatcher.filters.state import StatesGroup, State


class AddChannels(StatesGroup):
    user_channels = State()


class PostChannelUser(StatesGroup):
    text = State()
    channel = State()
    confirmation = State()
    data_time = State()


class ActionForTask(StatesGroup):
    action = State()
    data_time = State()
