from models import User
from schemas.user import UserSchema
from schemas.dto.user import UserCreateDto, UserUpdateDto
from typing import List
import json

from tortoise.exceptions import DoesNotExist, ValidationError

from loguru import logger


from redis.asyncio import Redis
from backend.config import Redis as RedisConfig


class UserService():
    prefetch_list = ['sessions', 'channels', 'news']

    @classmethod
    async def get_all(cls) -> List[UserSchema]:
        '''Get all users'''
        users = await User.all().prefetch_related(*cls.prefetch_list)
        return [await users.to_schema() for users in users]


    @classmethod
    async def get(cls, id: str) -> UserSchema:
        '''Get user by uuid'''
        user = await cls.redis_get(id)
        
        if (user is None) or (user == {}):
            user = await User.get_or_none(id=id).prefetch_related(*cls.prefetch_list)
            if user is None: raise DoesNotExist(f'pk={id} | User not found')
            await cls.redis_set(user.id, await user.to_json())

        return user

    
    @classmethod
    async def get_by_user_id(cls, user_id: int) -> UserSchema:
        '''Get user by unique Telegram ID'''
        id = await cls.find_to_pk('user_id', user_id)
        user = await cls.redis_get(id)

        if (user is None) or (user == {}):
            user = await User.get_or_none(user_id=user_id).prefetch_related(*cls.prefetch_list)
            if user is None: raise DoesNotExist(f'user_id={user_id} | User not found')
            await cls.redis_set(id, await user.to_json())

        return user
    

    @classmethod
    async def get_by_yandex_id(cls, yandex_id: str) -> UserSchema:
        '''Get user by unique Yandex ID'''
        id = await cls.find_to_pk('yandex_id', yandex_id)
        user = await cls.redis_get(id)

        if (user is None) or (user == {}):
            user = await User.get_or_none(yandex_id=yandex_id).prefetch_related(*cls.prefetch_list)
            if user is None: raise DoesNotExist(f'yandex_id={id} | User not found')
            await cls.redis_set(id, await user.to_json())

        return user
    

    @classmethod
    async def create(cls, dto: UserCreateDto) -> None:
        '''Create user'''
        user = await User.create(
            user_id=dto.user_id,
            email=dto.email,
            full_name=dto.full_name,
            username=dto.username,
        )


    @classmethod
    async def update(cls, id: str, dto: UserUpdateDto) -> UserSchema:
        '''Update user from body'''
        user = await User.get_or_none(id=id)
        if user is None: raise DoesNotExist(f'pk={id} | User not found')
        await user.update_from_dict(dto.model_dump())
        await user.save()
        user = user.prefetch_related(*cls.prefetch_list)
        await cls.redis_update(id, await user.to_json())

        return user

    
    @classmethod
    async def delete(cls, id: str):
        '''Delete user by uuid'''
        user = await User.get_or_none(id=id)
        if user is None: raise DoesNotExist(f'pk={id} | User not found')
        await cls.delete(id)

        await user.delete()

    
    @staticmethod
    async def find_to_pk(field: str, value: str) -> str:
        '''
        Find user by field and return pk:\n
        * user_id
        * yandex_id
        '''

        allowed_fields = ['user_id', 'yandex_id']

        if field not in allowed_fields:
            raise ValueError(f"Invalid field. Allowed values are: {', '.join(allowed_fields)}")
        
        if field == 'user_id':
            return (await User.get(user_id=value)).id
        elif field == 'yandex_id':
            return (await User.get(yandex_id=value)).id

    
    # Redis
    @staticmethod
    async def redis_connect() -> Redis:
        '''Connect to redis\n:return Redis instance'''
        return Redis(host=RedisConfig.host, port=RedisConfig.port)
    

    @staticmethod
    async def redis_close(redis: Redis) -> None:
        redis.close()


    @classmethod
    async def redis_get(cls, key: str) -> UserSchema:
        redis = await cls.redis_connect()

        user_json = await redis.get(key)
        if (user_json is None) or (user_json == {}): return None

        user_json = user_json.decode('utf-8')
        user = json.loads(user_json)
        
        return UserSchema(**user)


    @classmethod
    async def redis_set(cls, key: str, value) -> None:
        redis = await cls.redis_connect()

        if isinstance(value, dict):
            value = json.dumps(value)
        else:
            value = str(value)

        await redis.set(key, value)
        logger.info('set seccessful')

    
    @classmethod
    async def redis_update(cls, key: str, new_value) -> None:
        redis = await cls.redis_connect()

        if isinstance(value, dict):
            value = json.dumps(value)
        else:
            value = str(value)

        await redis.set(key, new_value)

    
    @classmethod
    async def redis_delete(cls, key: str) -> None:
        redis = await cls.redis_connect()

        await redis.delete(key)
    