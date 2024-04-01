import aiohttp
from data.config import API
from loguru import logger

from .exceptions import DeleteException


class ChannelService:
    @staticmethod
    async def create_channel(title: str, channel_id: str, user_id: int):
        header = {
            "Content-Type": "application/json"
        }
        data = {
            "title": title,
            "channel_id": channel_id,
            "user_id": user_id
        }
        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.post(url=API.base_url + 'channel', json=data)

            if response.status == 200 or 201:
                return await response.json()
            else:
                logger.error(f'[{response.status}] {await response.json()}')
    
    @staticmethod
    async def findOneById(id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + 'channel/' + str(id))

            if response.status == 200:
                return await response.json()
            else:
                logger.error(f'[{response.status}] {await response.json()}')

    @staticmethod
    async def toggle(id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=API.base_url + 'channel/toggle/' + str(id))

            if response.status == 200 or 201:
                return await response.json()
            else:
                logger.error(f'[{response.status}] {await response.json()}')

    @staticmethod
    async def delete(id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.delete(url=API.base_url + 'channel/' + str(id))

            if response.status != 204:
                raise DeleteException(f'[{response.status}] Ошибка при удалении канала', extra_info=await response.json())
