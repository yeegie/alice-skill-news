import aiohttp
from data.config import API
from loguru import logger

from typing import Optional

from .exceptions import DeleteException


class UserService:
    @staticmethod
    async def create_user(user_id: int, email: str, username: str, full_name: str):
        """
        ababab
        """
        header = {
            "Content-Type": "application/json"
        }
        data = {
            "user_id": user_id,
            "email": email,
            "full_name": full_name,
            "username": username,
        }
        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.post(url=API.base_url + 'users', json=data)

            if response.status == 200 or 201:
                return await response.json()
            else:
                logger.error(f'[{response.status}] {response.json()}')

    @staticmethod
    async def findOneByUserId(user_id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + f'users/by/user_id/{user_id}')

            if response.status == 200:
                return await response.json()
            elif response.status == 404:
                return 404
            else:
                logger.error(f'[{response.status}] {response.json()}')

    @staticmethod
    async def delete(id: str):
        async with aiohttp.ClientSession() as session:
            response = await session.delete(url=API.base_url + f'users/{id}')

            if response.status != 204:
                raise DeleteException(f'[{response.status}] Ошибка при удалении пользователя', await response.json())
            

    @staticmethod
    async def check(user_id: str):
        '''
        : return status_code, user_data if exist
        '''
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + f'users/by/user_id/{user_id}')
            if response.status == 404:
                return False, None
            elif response.status == 200:
                return True, await response.json()
    
    class UserDto:
        type = Optional[str]
        username = Optional[str]
        name = Optional[str]

    @staticmethod
    async def update(id: int, data: Optional[UserDto] = None):
        '''
        id: user uuid
        data: UserDto
        '''
        header = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.patch(url=API.base_url + f'user/' + str(int), data=data)

