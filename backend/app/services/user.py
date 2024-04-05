from models import User
from schemas.user import UserSchema
from schemas.dto.user import UserCreateDto, UserUpdateDto
from typing import List

from tortoise.exceptions import DoesNotExist, ValidationError

from loguru import logger


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
        user = await User.get_or_none(id=id).prefetch_related(*cls.prefetch_list)
        if user is None: raise DoesNotExist(f'pk={id} | User not found')
        return await user.to_schema()

    
    @classmethod
    async def get_by_user_id(cls, user_id: int) -> UserSchema:
        '''Get user by unique Telegram ID'''
        user = await User.get_or_none(user_id=user_id).prefetch_related(*cls.prefetch_list)
        if user is None: raise DoesNotExist(f'user_id={user_id} | User not found')
        return await user.to_schema()
    

    @classmethod
    async def get_by_yandex_id(cls, yandex_id: str) -> UserSchema:
        '''Get user by unique Yandex ID'''
        user = await User.get_or_none(yandex_id=yandex_id).prefetch_related(*cls.prefetch_list)
        if user is None: raise DoesNotExist(f'yandex_id={id} | User not found')
        return await user.to_schema()
    

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
        return user.prefetch_related(*cls.prefetch_list)

    
    @classmethod
    async def delete(cls, id: str):
        '''Delete user by uuid'''
        user = await User.get_or_none(id=id)
        logger.info(f'{user} | {user is None}')
        if user is None: raise DoesNotExist(f'pk={id} | User not found')
        await user.delete()
    