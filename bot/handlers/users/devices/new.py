from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from helpers.keyboards import markups
from helpers.fabrics import DeviceCallback
from helpers.functions.word_generator import WordGenerator

from services.session_service import SessionService

from handlers.routers import user_router


class LinkDevice(StatesGroup):
    confirm = State()


async def create_session(message: Message, user_id: int):
    secret_word = WordGenerator.generate()
    is_exist, session = await SessionService.check(message.from_user.id)
    
    if is_exist:
        await message.answer('У вас есть активная сессия, вы не можете одновременно связывать несколько устройства 🙄', reply_markup=markups.cancel_all_sessions())
        return
    else:
        await SessionService.create(user_id=user_id, secret=secret_word)
        await message.answer('Вот твоя секретная фраза, она действует 3 минуты 🔗')
        await message.answer(f'<code>{secret_word}</code>')
        



@user_router.callback_query(DeviceCallback.filter(F.action == 'new'))
async def new_device(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer('Как выглядит процесс связывания с умным устройством\n1. Скажи — Алиса, запусти навык «Новости из Телеграм».\n2. Затем — Алиса, связать устройства.\n4. Алиса попросит секретную фразу, которую я тебе скажу далее\n\nПродолжаем?', reply_markup=markups.confirm())
    await state.set_state(LinkDevice.confirm)
    await bot.answer_callback_query(callback.id)


@user_router.message(LinkDevice.confirm)
async def get_confirm(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == 'да':
        await create_session(message, message.from_user.id)
        await state.clear()
    elif message.text.lower() == 'нет':
        await message.answer('👌')
        await state.clear()
    else:
        await message.answer('Я тебя не понял 🤨')
