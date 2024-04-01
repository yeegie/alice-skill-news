from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers.fabrics import ChannelsCallback
from helpers.functions import edit_message
from helpers.keyboards import markups

from handlers.routers import user_router

from services.channel_service import ChannelService


@user_router.callback_query(ChannelsCallback.filter(F.action == 'open'))
async def open(callback: CallbackQuery, callback_data: ChannelsCallback, bot: Bot):
    channel = await ChannelService.findOneById(callback_data.channel_id)
    await bot.answer_callback_query(callback.id)
    await edit_message(
        message=callback.message,
        text=f"{channel['title']} : {channel['channel_id']}",
        reply_markup=markups.channel_view(channel['id'], channel['active'])
        )
