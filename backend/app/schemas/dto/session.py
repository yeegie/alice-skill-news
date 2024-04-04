from pydantic import BaseModel


class SessionAnswerDto(BaseModel):
    secret: str
    yandex_id: str


class SessionCreateDto(BaseModel):
    user_id: int
    secret: str


class SessionUpdateDto(BaseModel):
    pass
