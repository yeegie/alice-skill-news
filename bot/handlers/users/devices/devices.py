from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery

from aiogram.filters import Command

from helpers.keyboards import markups
from helpers.functions import render_devices

from handlers.routers import user_router

from services import UserService


@user_router.message(F.text.lower().startswith('устройства'))
@user_router.message(Command(commands=['devices']))
async def open_devices(message: Message, bot: Bot):
    devices = (await UserService.findOneByUserId(message.from_user.id))['devices']
    await render_devices(message, devices)
