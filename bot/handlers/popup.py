from aiogram import Bot, F
from aiogram.types import CallbackQuery

from helpers.fabrics import PopupCallback

from .routers import user_router


@user_router.callback_query(PopupCallback.filter(F.action == 'close'))
async def delete_popup(callback: CallbackQuery, callback_data: PopupCallback, bot: Bot):
    await bot.delete_message(callback.message.chat.id, callback_data.message_id)
    await bot.answer_callback_query(callback.id)
