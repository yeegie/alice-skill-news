from aiogram.types import Message
from datetime import datetime

from models.schemas.user import UserSchema


async def render_profile(message, markup, user_data: UserSchema):
    message_text = f"""
👤 Ваше имя: {user_data.full_name}

📫 Почта : {user_data.email}
📆 Дата регистрации: {user_data.register_time.strftime('%d.%m.%Y')}

🔗 ЯндексID: <code>{user_data.yandex_id if user_data.yandex_id is not None else 'не привязан'}</code>

🔐: <code>{user_data.id}</code>
"""

    await message.answer(message_text, reply_markup=markup, protect_content=True)
