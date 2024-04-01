from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery

from helpers.fabrics import DeviceCallback
from helpers.functions import render_devices

from services.session_service import SessionService
from services.user_service import UserService

from handlers.routers import user_router

@user_router.callback_query(DeviceCallback.filter(F.action == 'close_all_sessions'))
async def close_all_sessions(callback: CallbackQuery, bot: Bot):
    await SessionService.close_all_sessions(callback.from_user.id)
    devices = (await UserService.findOneByUserId(callback.from_user.id))['devices']

    await callback.message.answer('Закрыл все сессии 👌')
    await render_devices(callback.message, devices)
    await bot.answer_callback_query(callback.id)
