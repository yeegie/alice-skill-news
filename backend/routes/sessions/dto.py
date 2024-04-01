from pydantic import BaseModel
from datetime import datetime


class SessionSchema(BaseModel):
    id: str
    secret: str
    start_time: datetime
    end_time: datetime
    user_id: int
    active: bool


class SessionAnswerDto(BaseModel):
    secret: str
    yandex_id: str


class SessionCreateDto(BaseModel):
    user_id: int


class SessionUpdateDto(BaseModel):
    pass
