from aiogram.filters.callback_data import CallbackData
from typing import Optional

class MenuCallback(CallbackData, prefix='menu'):
    action: str
    value: Optional[str] = None

class ChannelsCallback(CallbackData, prefix='channels'):
    action: str
    target: Optional[str] = None
    channel_id: Optional[str] = None

class PopupCallback(CallbackData, prefix='popup'):
    action: str
    message_id: int

class SessionCallback(CallbackData, prefix='session'):
    action: str
    session_id: Optional[str] = None
    