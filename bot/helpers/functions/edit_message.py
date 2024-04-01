from aiogram import Bot
from aiogram.types import Message

from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardMarkup

async def edit_message(message: Message, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None):
    await message.edit_text(
        text=text,
        reply_markup=reply_markup
    )