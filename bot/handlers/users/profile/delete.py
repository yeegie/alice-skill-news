from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers.fabrics.fabric import MenuCallback
from helpers.keyboards import markups
from helpers.functions import render_profile

from services.user_service import UserService

from handlers.routers import user_router

from aiogram.fsm.state import State, StatesGroup

from loguru import logger

class ConfirmDeleteProfile(StatesGroup):
    confirm = State()


@user_router.callback_query(MenuCallback.filter(F.action == 'delete_profile'))
async def delete_profile(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=markups.cry())
    await callback.message.answer('Профиль невозможно будет восстановить, вся информация о подписках и устройствах будет <b>удалена</b>, ты уверен?', reply_markup=markups.confirm())
    await state.set_state(ConfirmDeleteProfile.confirm)
    await bot.answer_callback_query(callback.id)


@user_router.message(ConfirmDeleteProfile.confirm)
async def get_confirm(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == 'да':
        user = await UserService.findOneByUserId(user_id=message.from_user.id)
        try:
            await UserService.delete(user['id'])
            await message.answer('Твой профиль удалён 👋')
            await state.clear()
        except Exception as ex:
            await message.answer('Технические неполадки 🪛')
            await state.clear()
            logger.error(f'{ex}\nResponse: {ex.extra_info}')

    elif message.text.lower() == 'нет':
        user = await UserService.findOneByUserId(user_id=message.from_user.id)
        await render_profile(message, markups.profile_menu(), user)
        await state.clear()
    else:
        await message.answer('Я тебя не понял 🤔', reply_markup=markups.confirm())
