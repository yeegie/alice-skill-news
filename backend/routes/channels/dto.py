from pydantic import BaseModel


class ChannelSchema(BaseModel):
    id: str
    title: str
    channel_id: str
    user_id: int
    active: bool


class ChannelCreateDto(BaseModel):
    title: str
    channel_id: str
    user_id: int
