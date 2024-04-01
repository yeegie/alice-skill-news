from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from ..sessions.dto import SessionSchema as Session
from ..channels.dto import ChannelSchema as Channel
from ..news.dto import NewsSchema as News


class UserSchema(BaseModel):
    id: str
    type: str
    user_id: int
    yandex_id: Optional[str] = None
    full_name: str
    username: Optional[str] = None
    email: EmailStr
    register_time: datetime
    sessions: List[Session]
    channels: List[Channel]
    news: List[News]
    

class UserCreateDto(BaseModel):
    user_id: int
    email: EmailStr
    full_name: str
    username: str


class UserUpdateDto(BaseModel):
    type: str
    email: EmailStr
    full_name: str
    username: Optional[str] = None
