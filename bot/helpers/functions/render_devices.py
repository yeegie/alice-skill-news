from aiogram.types import Message
from helpers.keyboards import markups

async def render_devices(message: Message, devices: list):
    if devices:
        await message.answer('Ваши устройства 💻🖥📱', reply_markup=markups.devices_list(devices))
    else:
        await message.answer('Тут пусто 🕸', reply_markup=markups.device_menu())