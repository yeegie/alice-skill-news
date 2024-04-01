from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from helpers.fabrics import MenuCallback
from helpers.keyboards import markups

from typing import Union

from ..routers import user_router


@user_router.message(Command(commands=['start']))
async def welcome(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer('📰')
    await message.answer(f'''Привет ✋\n\nЧтобы ты мог получать новости из нашего любимого мессенджера телеграм, необходимо зарегестрироваться, начнём?''', reply_markup=markups.welcome())


@user_router.message(Command(commands=['help']))
@user_router.message(F.text.lower().startswith('помощь'))
async def welcome(message: Message, bot: Bot, state: FSMContext):
    await message.answer('🔍')
    await message.answer(f'''
<b>Помощь</b>
1. Для начала зарегестрируйся - /profile.
2. После успешной регистрации перейди в подписки - /subscriptions, нажми <code>добавить</code>.
3. Перешли сообщение от канала, или его id.
4. Затем перейди в <code>мои устройства</code> - /devices и нажми <code>связать</code>, тебе будет передан набор слов, запомни, они понадобятся.
5. Запусти навык <code>новости из телеграм</code>, и скажи <code>связать</code>, Алиса попросит тот самый набор слов из прошлого шага, скажи их.
6. ...
''')


@user_router.message(Command(commands=['menu']))
@user_router.message(F.text.lower().startswith('меню'))
async def help(message: Message, bot: Bot):
    await message.answer(text='Используй кнопки ниже для навигации по меню 🕹', reply_markup=markups.menu())


@user_router.callback_query(MenuCallback.filter(F.action == 'open_menu'))
async def help_cb(callback: CallbackQuery, bot: Bot):
    await callback.message.answer(text='Используй кнопки ниже для навигации по меню 🕹', reply_markup=markups.menu())
    await bot.answer_callback_query(callback.id)


@user_router.message(F.text.lower().startswith('отмена'))
async def help(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer('👌')
