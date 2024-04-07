from pydantic import BaseModel
from datetime import datetime


class SessionSchema(BaseModel):
    id: str
    secret: str
    start_time: datetime
    end_time: datetime
    user_id: int
    active: bool
