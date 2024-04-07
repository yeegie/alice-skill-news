import aiohttp
from data.config import API
from loguru import logger

from typing import Optional
from models.schemas.user import UserSchema

from .exceptions import DeleteException, NotFound


class UserService:
    @staticmethod
    async def create(user_id: int, email: str, username: str, full_name: str):
        """
        Create user from data\n
        params:
        * user_id -- telegram unique id
        * email -- just email
        * username -- telegram username start with "@", can be None
        * full_name -- full_name from user.full_name
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
    async def get(user_id: int) -> UserSchema:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=API.base_url + f'users/by-user_id/{user_id}')
            response_raw = await response.json()

            if response.status == 200:
                return UserSchema(
                    id = response_raw['id'],
                    type = response_raw['type'],
                    user_id = response_raw['user_id'],
                    yandex_id = response_raw['yandex_id'],
                    full_name = response_raw['full_name'],
                    username = response_raw['username'],
                    email = response_raw['email'],
                    register_time = response_raw['register_time'],
                    sessions = response_raw['sessions'],
                    channels = response_raw['channels'],
                    news = response_raw['news'],

                )
            elif response.status == 404:
                return None
            elif response.status == 500:
                logger.error(f'[500] USER NOT FOUND\n{await response.json()}')
                return None
            else:
                logger.error(f'[{response.status}] Unknown error\n{await response.json()}')
                return None
            

    @classmethod
    async def exist(cls, user_id: int):
        user = await cls.get(user_id)

        if user is None:
            return False
        
        return True


    @staticmethod
    async def delete(id: str):
        async with aiohttp.ClientSession() as session:
            response = await session.delete(url=API.base_url + f'users/{id}')

            if response.status != 204:
                raise DeleteException(f'[{response.status}] Ошибка при удалении пользователя', await response.json())
            
    
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

