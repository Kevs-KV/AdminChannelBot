from aiogram.dispatcher.filters.state import StatesGroup, State


class LanguageUser(StatesGroup):
    start = State()
    language = State()
