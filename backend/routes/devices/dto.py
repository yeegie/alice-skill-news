from pydantic import BaseModel
from datetime import datetime


class DeviceSchema(BaseModel):
    id: str
    title: str
    user_id: int
    register_time: datetime


class DeviceCreateDto(BaseModel):
    title: str
    user_id: int


class DeviceUpdateDto(BaseModel):
    title: str
