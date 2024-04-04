from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery, InputTextMessageContent, InlineQueryResultArticle

from handlers.routers import user_router

from pprint import pprint
from loguru import logger


# @user_router.callback_query()
# async def cb_handler(callback: CallbackQuery):
#     logger.warning('CALLBACK HANDLER')
#     pprint(callback)

# @user_router.message()
# async def msg_handler(message: Message, bot: Bot):
#     logger.warning('MESSAGE HANDLER')
#     await message.answer(message.text)

