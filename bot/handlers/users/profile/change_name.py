from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.user_service import UserService

from helpers.fabrics import MenuCallback
from helpers.keyboards import markups
from helpers.functions import render_profile
from handlers.routers import user_router


class ChangeName(StatesGroup):
    new_name = State()
    confirm = State()


@user_router.callback_query(MenuCallback.filter(F.action == 'edit_name'))
async def change_name(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer('Введи имя которое будет произносить Алиса:')
    await state.set_state(ChangeName.new_name)
    await bot.answer_callback_query(callback.id)

@user_router.message(ChangeName.new_name)
async def get_name(message: Message, bot: Bot, state: FSMContext):
    new_name = message.text
    await message.answer(f'Ты ввёл <code>{new_name}</code>, записываю?', reply_markup=markups.confirm())
    await state.update_data(new_name=new_name)
    await state.set_state(ChangeName.confirm)

@user_router.message(ChangeName.confirm)
async def get_confirm(message: Message, state: FSMContext, bot: Bot):
    new_name = (await state.get_data())['new_name']
    if message.text.lower() == 'да':
        is_exist, user = await UserService.exist(user_id=message.from_user.id)
        # user = await UserService.getByUserId(message.from_user.id)
        # await UserService.update(user['id'], {'name': 'new_name'})
        # await render_profile(message, markups.menu(), user)
        await message.answer('👌')
        await render_profile(message, markups.profile_menu(), user)
        await state.clear()
    elif message.text.lower() == 'нет':
        await message.answer('Введи ещё раз')
        await state.set_state(ChangeName.new_name)
    else:
        await message.answer('Я тебя не понял')
