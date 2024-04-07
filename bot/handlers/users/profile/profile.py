from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from helpers.keyboards import markups
from helpers.fabrics.fabric import MenuCallback

from handlers.routers import user_router

from services.user_service import UserService
from aiogram.utils import markdown

from datetime import datetime

from helpers import states

from helpers.functions import render_profile


@user_router.message(F.text.lower().startswith('профиль'))
@user_router.message(Command(commands=['profile']))
async def show_profile(message: Message):
    user = await UserService.get(user_id=message.from_user.id)

    if user is not None:
        await render_profile(message, markups.profile_menu(), user)
    else:
        await message.answer('У вас нет профиля!', reply_markup=markups.welcome())


@user_router.callback_query(MenuCallback.filter(F.action == 'edit_profile'))
async def open_profile_menu(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_reply_markup(reply_markup=markups.profile_menu_list())
    await bot.answer_callback_query(callback.id)
