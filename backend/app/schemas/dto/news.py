from pydantic import BaseModel


class NewsCreateDto(BaseModel):
    user_id: str


class NewsUpdateDto(BaseModel):
    pass
