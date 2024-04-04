from pydantic import BaseModel


class ChannelCreateDto(BaseModel):
    title: str
    channel_id: str
    user_id: int
