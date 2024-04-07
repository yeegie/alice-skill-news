import aiohttp
from data.config import API
from loguru import logger

from .exceptions import DeleteException

from models.schemas.channel import ChannelSchema


class ChannelService:
    @staticmethod
    async def create(title: str, channel_id: str, user_id: int):
        header = {
            "Content-Type": "application/json"
        }
        data = {
            "title": title,
            "channel_id": channel_id,
            "user_id": user_id
        }
        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.post(url=API.base_url + 'channels', json=data)

            if response.status == 200 or 201:
                return await response.json()
            else:
                logger.error(f'[{response.status}] {await response.json()}')
    
    @staticmethod
    async def get(id: str) -> ChannelSchema:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + 'channels/' + id)
            response_raw = await response.json()

            if response.status == 200:
                return ChannelSchema(
                    id=response_raw['id'],
                    title=response_raw['title'],
                    channel_id=response_raw['channel_id'],
                    user_id=response_raw['user_id'],
                    active=response_raw['active'],
                )
            else:
                logger.error(f'[{response.status}] {await response.json()}')

    @staticmethod
    async def toggle(id: str):
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=API.base_url + 'channels/toggle/' + id)

            if response.status == 200 or 201:
                return await response.json()
            else:
                logger.error(f'[{response.status}] {await response.json()}')

    @staticmethod
    async def delete(id: str):
        async with aiohttp.ClientSession() as session:
            response = await session.delete(url=API.base_url + 'channels/' + id)

            if response.status != 204:
                raise DeleteException(f'[{response.status}] Ошибка при удалении канала', extra_info=await response.json())
