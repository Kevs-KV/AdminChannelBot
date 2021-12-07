import pytz
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from odmantic import AIOEngine

from app.keyboards.inline import ChoiceLanguageUser
from app.models import UserModel
from app.states.language_states import LanguageUser


async def get_start_message(message: Message):
    markup = ChoiceLanguageUser().get()
    await message.answer(
        "🇷🇺 Выберите язык:\n\n" "🇬🇧 Choose your language:",
        reply_markup=markup,
    )
    await LanguageUser.start.set()


async def set_user_language(
        query: CallbackQuery, db: AIOEngine, callback_data: dict, user: UserModel, state: FSMContext
):
    await query.answer()
    language = callback_data.get("language")
    user.language = language
    await db.save(user)
    _ = i18n = query.bot["i18n"]
    i18n.ctx_locale.set(language)
    await query.message.edit_text(
        _(
            "Привет! Данный бот предназначен для администрования телеграм каналов, для списка команды введите - /help",
        )
    )
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")
    dp.register_callback_query_handler(set_user_language, ChoiceLanguageUser.callback_data.filter(),
                                       state=LanguageUser.start)
