from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsSchema(BaseModel):
    id: int
    last_update: datetime
    last_news: Optional[list] = None
    user_id: str


class NewsCreateDto(BaseModel):
    user_id: str


class NewsUpdateDto(BaseModel):
    pass
