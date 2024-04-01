from aiogram.types import Message
from datetime import datetime

async def render_profile(message, markup, user_data):
    register_time = (datetime.strptime(user_data['register_time'].split('T')[0], '%Y-%m-%d')).strftime('%d.%m.%Y')
    message_text = f"""
===== Ваш профиль 👤 =====
Ваше имя: {user_data['name']}
Email 📫: {user_data['email']}
Дата регистрации 📆: {register_time}

🔐: <code>{user_data['id']}</code>
==========================
"""

    await message.answer(message_text, reply_markup=markup, protect_content=True)
