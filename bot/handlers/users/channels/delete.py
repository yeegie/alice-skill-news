from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers.fabrics import ChannelsCallback
from helpers.keyboards import markups
from helpers.functions import render_channels

from services.channel_service import ChannelService
from services.user_service import UserService

from handlers.routers import user_router

from aiogram.fsm.state import State, StatesGroup


class ConfirmDeleteChannel(StatesGroup):
    confirm = State()


@user_router.callback_query(ChannelsCallback.filter(F.action == 'delete'))
async def delete_channel(callback: CallbackQuery, callback_data: ChannelsCallback, bot: Bot, state: FSMContext):
    channel = await ChannelService.findOneById(callback_data.channel_id)
    await callback.message.answer(f'Удалить канал {channel["title"]}?', reply_markup=markups.confirm())
    await state.set_state(ConfirmDeleteChannel.confirm)
    await state.update_data(channel_id=callback_data.channel_id)
    await bot.answer_callback_query(callback.id)


@user_router.message(ConfirmDeleteChannel.confirm)
async def get_confirm(message: Message, bot: Bot, state: FSMContext):
    channel_id = (await state.get_data())['channel_id']

    if message.text.lower() == 'да':
        await ChannelService.delete(channel_id)
        channels = (await UserService.findOneByUserId(user_id=message.from_user.id))['channels']

        await message.answer('Удалил')
        await state.clear()
        await render_channels(message, channels)
    elif message.text.lower() == 'нет':
        await message.answer('👌')
        await message.answer('Отмена', reply_markup=markups.menu())
        await state.clear()
    else:
        await message.answer('Не понял тебя 🤔')
