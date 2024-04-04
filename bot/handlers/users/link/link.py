from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from handlers.routers import user_router

from helpers.functions.word_generator import WordGenerator
from helpers.keyboards import markups
from helpers.fabrics import SessionCallback

from services.session_service import SessionService

from loguru import logger


class LinkState(StatesGroup):
    confirm = State()


@user_router.message(F.text.lower().startswith('связать'))
@user_router.message(Command(commands=['link']))
async def session(message: Message, state: FSMContext):
    await message.answer('Запустить процесс связывания аккаунта?', reply_markup=markups.confirm())
    await state.set_state(LinkState.confirm)


@user_router.message(LinkState.confirm)
async def get_confirm(message: Message, state: FSMContext):
    message_text = message.text.lower()

    if message_text == 'да':
        secret_word = WordGenerator.generate()
        is_exist, sessions = await SessionService.check(message.from_user.id)

        if is_exist:
            session_body = f'\n└ сессия <code>{sessions[0]["id"]}</code>'
            await message.answer(f'У вас уже есть активная сессия{session_body}', reply_markup=markups.cancel_all_sessions())
            await state.clear()
        else:
            session = await SessionService.create(message.from_user.id, secret_word)
            await message.answer('Я скажу тебе секретное слово, а ты назовешь его Алисе\n\n❗️ У тебя будет три минуты, по истечению времени сессия будет закрыта')
            await message.answer(f'<code>{secret_word}</code>', reply_markup=markups.cancel_all_sessions())

    elif message_text == 'нет':
        await message.answer('👌', reply_markup=markups.menu())
        await state.clear()
    else:
        await message.answer('Не понял твой ответ')


@user_router.callback_query(SessionCallback.filter(F.action == 'close_all_sessions'))
async def close_all_sessions(callback_query: CallbackQuery, callback_data: SessionCallback, bot: Bot):
    await SessionService.close_all_sessions(callback_query.from_user.id)
    await callback_query.message.answer('Закрыл все сессии 👌', reply_markup=markups.menu())
    await bot.answer_callback_query(callback_query.id)
