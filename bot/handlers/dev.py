from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery

from handlers.routers import user_router

from pprint import pprint
from loguru import logger


# @user_router.callback_query()
# async def cb_handler(callback: CallbackQuery):
#     logger.warning('CALLBACK HANDLER')
#     pprint(callback)

# @user_router.message()
# async def msg_handler(message: Message):
#     logger.warning('MESSAGE HANDLER')
#     pprint(message)
