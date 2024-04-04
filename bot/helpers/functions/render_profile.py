from aiogram.types import Message
from datetime import datetime

async def render_profile(message, markup, user_data):
    register_time = (datetime.strptime(user_data['register_time'].split('T')[0], '%Y-%m-%d')).strftime('%d.%m.%Y')
    message_text = f"""
👤 Ваше имя: {user_data['full_name']}

📫 Почта : {user_data['email']}
📆 Дата регистрации: {register_time}

🔗 ЯндексID: <code>{user_data['yandex_id'] if user_data['yandex_id'] is not None else 'не привязан'}</code>

🔐: <code>{user_data['id']}</code>
"""

    await message.answer(message_text, reply_markup=markup, protect_content=True)
