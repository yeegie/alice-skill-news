from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from loguru import logger

from helpers.keyboards import markups

from ..routers import user_router

from helpers import states

from helpers.smtp import SMTPService
from data.config import SMTP

from helpers.functions import WordGenerator

from services.user_service import UserService

from captcha.image import ImageCaptcha


@user_router.message(F.text == 'Регистрация 👤')
@user_router.message(F.text.lower().startswith('регистрация'))
@user_router.message(F.text == 'Другую капчу 🤬')
async def register_start(message: Message, bot: Bot, state: FSMContext):
    is_exist, user = await UserService.check(message.from_user.id)

    # Проверяем имеет ли пользователь аккаунт
    if is_exist:
        await message.answer('У вас уже есть профиль 🙄', reply_markup=markups.menu())
        return

    resource_dir = 'resources/'
    roboto = resource_dir + 'fonts/roboto-regular.ttf'
    image = ImageCaptcha(fonts=[roboto], width=250, height=100)

    captcha_code = WordGenerator.generate()
    await state.update_data(captcha=captcha_code)

    data = image.generate(captcha_code)
    image.write(captcha_code, resource_dir + f'captcha/image/{message.from_user.id}.png')

    # Take photo
    captcha_image = FSInputFile(resource_dir + f'captcha/image/{message.from_user.id}.png')
    await bot.send_photo(message.chat.id, captcha_image, caption='Введи капчу с картинки ✍️', reply_markup=markups.get_new_captcha())

    await state.set_state(states.Register.captcha)

@user_router.message(states.Register.captcha)
async def get_captha_code(message: Message, state: FSMContext):
    captcha = (await state.get_data())['captcha']

    if captcha == message.text:
        await message.answer('Введи свою почту на неё придёт код подтверждения, например\n└ <code>bob@gmail.com</code>\n\nВведи отмена, чтобы выйти')
        await state.set_state(states.Register.email)
    else:
        await message.answer('Не правильно, попробуй ещё раз', reply_markup=markups.get_new_captcha())

@user_router.message(states.Register.email)
async def get_email(message: Message, state: FSMContext):
    email = message.text.lower()

    if email.count('@') == 1:
        await state.update_data(email=email)
        await message.answer(f'Ты ввёл: <code>{email}</code>, отправляю код?', reply_markup=markups.confirm())
        await state.set_state(states.Register.confirm)
    else:
        await message.answer('Введи свою почту в таком формате\n└ <code>bob@gmail.com</code>\n\nНапомню, что ты можешь ввести отмена для выхода')

@user_router.message(states.Register.confirm)
async def get_confirm(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer('Так, отправляю...')

        smtp_service = SMTPService()

        data = await state.get_data()
        secret = await smtp_service.send_confirm_code(data['email'])
        logger.debug(f'[{message.from_user.id}] @{message.from_user.username} -- {secret}')

        await message.answer(f'Отправил, жду твой код')
        await state.update_data(secret=secret)

        await state.set_state(states.Register.code)
    elif message.text.lower() == 'нет':
        await message.answer('Введи свою почту на неё придёт код подтверждения, например\n└ <code>bob@gmail.com</code>')
        await state.set_state(states.Register.email)
    else:
        await message.answer('Не понял твоего ответа', reply_markup=markups.confirm())

@user_router.message(states.Register.code)
async def get_code(message: Message, state: FSMContext):
    user_code = message.text
    data = await state.get_data()

    if data['secret'] == user_code:
        await message.answer('Отлично, теперь добавь каналы которые ты хочешь отслеживать ⭐', reply_markup=markups.menu())
        response = await UserService.create_user(
            user_id=message.from_user.id,
            email=data['email'],
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        await state.clear()
    else:
        await message.answer('Не верный код!')
        await state.set_state(states.Register.code)
