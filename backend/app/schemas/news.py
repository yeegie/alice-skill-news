from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsSchema(BaseModel):
    id: int
    last_update: datetime
    last_news: Optional[list] = None
    user_id: str
