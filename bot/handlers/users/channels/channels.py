from aiogram import Bot, F
from aiogram.types import Message
from aiogram.filters import Command

from services.user_service import UserService

from helpers.functions import render_channels

from handlers.routers import user_router


@user_router.message(F.text.lower().startswith('каналы'))
@user_router.message(Command(commands=['channels']))
async def open_channels(message: Message, bot: Bot):
    user = await UserService.get(message.from_user.id)
    if user is not None:
        await render_channels(message, user.channels)
