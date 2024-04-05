from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from .session import SessionSchema
from .channel import ChannelSchema
from .news import NewsSchema


class UserSchema(BaseModel):
    id: str
    type: str
    user_id: int
    yandex_id: Optional[str] = None
    full_name: str
    username: Optional[str] = None
    email: EmailStr
    register_time: datetime
    sessions: List[SessionSchema]
    channels: List[ChannelSchema]
    news: List[NewsSchema]
