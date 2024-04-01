from aiogram import Bot, F
from aiogram.types import CallbackQuery

from handlers.routers import user_router

from helpers.fabrics.fabric import MenuCallback
from helpers.keyboards import markups


@user_router.callback_query(MenuCallback.filter(F.action == 'cancel'))
async def cancel(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_reply_markup(reply_markup=markups.profile_menu())
    await bot.answer_callback_query(callback.id)
