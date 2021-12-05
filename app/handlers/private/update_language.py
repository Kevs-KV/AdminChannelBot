from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from odmantic import AIOEngine

from app.keyboards.inline import ChoiceLanguageUser
from app.middlewares import i18n
from app.models import UserModel
from app.states.language_states import LanguageUser


async def choice_language(m: Message, _: i18n):
    markup = ChoiceLanguageUser().get()
    await m.answer(_('Пришлите свой язык'), reply_markup=markup)
    await LanguageUser.language.set()


async def save_language_user(query: CallbackQuery, user: UserModel, db: AIOEngine, state: FSMContext,
                             callback_data: dict, _: i18n):
    user.language = callback_data['language']
    await db.save(user)
    await query.message.answer(_('Язык установлен', locale=user.language))
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(choice_language, commands='update_language')
    dp.register_callback_query_handler(save_language_user, ChoiceLanguageUser.callback_data.filter(), state=LanguageUser.language)
