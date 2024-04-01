from data.config import API
from datetime import datetime
import aiohttp
from loguru import logger
from datetime import datetime, timedelta
from .exceptions import NotFoundException, ServerError


class SessionService:
    @staticmethod
    async def create(user_id: int, secret: str, live_time: int = 3):
        date_end = (datetime.now() + timedelta(minutes=live_time)).isoformat() + 'Z'

        header = {
            "Content-Type": "application/json"
        }

        data = {
            "user_id": user_id,
            "secret": secret,
            "endTime": date_end
        }
        
        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.post(url=API.base_url + 'session/', json=data)

            if response.status not in [200, 201]:
                logger.error(f'[{response.status}] An error occurred while creating a session.\nResponse: {await response.json()}')

    @staticmethod
    async def check(user_id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + 'session/active/' + str(user_id))
            session_count = len(await response.json())

            # print(f'{session_count=}')

            if (response.status == 200) and (session_count > 0):  # Если у пользователя есть активные сессии - True и их кол-во > 0
                return (True, await response.json())
            else:
                return (False, None)
                
                
    @staticmethod
    async def close_all_sessions(user_id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.patch(url=API.base_url + 'session/close/' + str(user_id))

            if (response.status in [200, 201]):
                return response.status
            else:
                logger.error(f'[{response.status}] An error occurred while closing a session.')
