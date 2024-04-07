from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers.fabrics import ChannelsCallback
from helpers.keyboards import markups
from helpers.functions import render_channels

from services.user_service import UserService

from handlers.routers import user_router


@user_router.callback_query(ChannelsCallback.filter(F.action == 'cancel'))
async def back_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    channels = (await UserService.get(callback.from_user.id)).channels
    await render_channels(callback.message, channels)
    await bot.answer_callback_query(callback.id)


@user_router.callback_query(ChannelsCallback.filter(F.action == 'back'))
async def open(callback: CallbackQuery, callback_data: ChannelsCallback, bot: Bot, state: FSMContext):
    await state.clear()
    channels = (await UserService.get(callback.from_user.id)).channels
    await render_channels(callback.message, channels, True)