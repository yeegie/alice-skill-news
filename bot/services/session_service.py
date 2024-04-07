from data.config import API
from datetime import datetime
import aiohttp
from loguru import logger
from datetime import datetime, timedelta
from .exceptions import NotFound, ServerError
from typing import Union, Tuple


class SessionService:
    @staticmethod
    async def create(user_id: int, secret: str):
        header = {
            "Content-Type": "application/json"
        }

        data = {
            "user_id": user_id,
            "secret": secret,
        }
        
        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.post(url=API.base_url + 'sessions/', json=data)

            if response.status not in [200, 201]:
                logger.error(f'[{response.status}] An error occurred while creating a session.\nResponse: {await response.json()}')

    @staticmethod
    async def check(user_id: int) -> Tuple[bool, Union[None, dict]]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + 'sessions/active/' + str(user_id))
            
            if response.status == 200:
                return (True, await response.json())
            elif response.status == 404:
                return (False, None)
            else:
                logger.error(f'[!] CHECK ERR\n{await response.json()}')
                
                
    @staticmethod
    async def close_all_sessions(user_id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.patch(url=API.base_url + 'sessions/close_all/' + str(user_id))

            if (response.status == 204):
                pass
            else:
                logger.error(f'[{response.status}] An error occurred while closing a session.')
