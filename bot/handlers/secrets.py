from aiogram import Bot, F
from aiogram.types import Message

from handlers.routers import user_router


sweet_words = ['cookie', 'cookies']

@user_router.message((F.text.lower().in_(sweet_words) | F.text.lower().startswith('cookie')))
async def sweet_words_handler(message: Message, bot: Bot):
    await message.answer('🍪')
