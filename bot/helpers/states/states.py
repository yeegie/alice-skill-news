from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    captcha = State()
    email = State()
    confirm = State()
    code = State()


class NewChannel(StatesGroup):
    channel_id = State()
    title = State()
    confirm = State()
