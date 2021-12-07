from aiogram.dispatcher.filters.state import StatesGroup, State


class TimezoneUser(StatesGroup):
    timezone = State()
