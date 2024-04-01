from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command

from helpers.fabrics import ChannelsCallback
from helpers import states
from helpers.keyboards import markups

from handlers.routers import user_router

from services import ChannelService


@user_router.callback_query(ChannelsCallback.filter(F.action == 'new'))
async def new_channel(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer('<b>Пришли мне ссылку на канал в формате:</b>\n\n<code>https://t.me/channel_name</code>\n<code>@channel_name</code>\n\n🔓 Канал должен быть публичным, иначе я не смогу получить доступ к постам', reply_markup=markups.back_to_channels_list())
    await state.set_state(states.NewChannel.channel_id)
    await bot.answer_callback_query(callback.id)


@user_router.message(states.NewChannel.channel_id)
async def get_channel(message: Message, bot: Bot, state: FSMContext):
    channel_name = message.text.replace('https://t.me/', '').lower()
    if channel_name[0] != '@': channel_name = '@' + channel_name
    await state.update_data(channel_id=channel_name)

    await message.answer('Теперь введи название канала, Алиса будет произносить их так как ты их назавешь')
    await state.set_state(states.NewChannel.title)


@user_router.message(states.NewChannel.title)
async def get_title(message: Message, bot: Bot, state: FSMContext):
    title = message.text
    channel_id = (await state.get_data())['channel_id']
    await state.update_data(title=title)
    await message.answer(f'<code>{title}</code> : <code>{channel_id}</code>\nВерно?', reply_markup=markups.confirm())
    await state.set_state(states.NewChannel.confirm)


@user_router.message(states.NewChannel.confirm)
async def confirm(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == 'да':
        data = await state.get_data()

        await ChannelService.create_channel(
            title=data['title'],
            channel_id=data['channel_id'],
            user_id=message.from_user.id,
        )
        await message.answer('Добавил 👌', reply_markup=markups.channels_end())
        await state.clear()
    elif message.text.lower() == 'нет':
        await message.answer('<b>Пришли мне ссылку на канал в формате:</b>\n\n<code>https://t.me/channel_name</code>\n<code>@channel_name</code>\n\n🔓 Канал должен быть публичным, иначе я не смогу получить доступ к постам')
        await state.set_state(states.NewChannel.channel_id)
    else:
        await message.answer('Не понял, напиши ещё раз')
