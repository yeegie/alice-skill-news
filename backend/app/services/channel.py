from schemas.channel import ChannelSchema
from schemas.dto.channel import ChannelCreateDto

from models.channels import Channel
from tortoise.exceptions import DoesNotExist

from typing import List

from .user import UserService


class ChannelService():
    @staticmethod
    async def create(dto: ChannelCreateDto):
        '''Create channel from dto'''
        channel = await Channel.create(
            title=dto.title,
            channel_id=dto.channel_id,
            user_id=dto.user_id,
        )
    

    @classmethod
    async def get(cls, id: str) -> ChannelSchema:
        '''Get channel by uuid'''
        channel = await Channel.get_or_none(id=id)

        if channel is None:
            raise DoesNotExist(f'pk={id} | Channel not found')
        return await channel.to_schema()
    

    @staticmethod
    async def all() -> List[ChannelSchema]:
        channels = await Channel.all()
        return [await channel.to_schema() for channel in channels]
    

    @staticmethod
    async def toggle(id: str):
        '''Toggle visibility (active) in channel by uuid'''
        channel = await Channel.get_or_none(id=id)
        if channel is None: raise DoesNotExist(f'pk={id} | Channel not found')
        await channel.toggle()


    @staticmethod
    async def delete(id: str):
        '''Delete channel by uuid'''
        channel = await Channel.get_or_none(id=id)
        if channel is None: raise DoesNotExist(f'pk={id} | Channel not found')
        await channel.delete()
