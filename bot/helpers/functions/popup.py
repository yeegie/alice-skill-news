from typing import Union
from aiogram.types import Message, CallbackQuery
from helpers.keyboards import markups


async def popup(message_text: str, message: Message):
    await message.answer(message_text, reply_markup=markups.popup(message.message_id + 1))
