from models import User
from schemas.user import UserSchema
from schemas.dto.user import UserCreateDto, UserUpdateDto

from tortoise.exceptions import DoesNotExist


class UserService():
    prefetch_list = ['sessions', 'channels', 'news']

    @classmethod
    async def get_user(cls, id: str) -> UserSchema:
        '''Get user by uuid'''
        user = await User.get_or_none(id=id).prefetch_related(*cls.prefetch_list)
        if user is None: raise DoesNotExist(f'[{id}] User not found')
        return user.to_schema()

    
    @classmethod
    async def get_user_by_user_id(cls, user_id: int) -> UserSchema:
        '''Get user by unique Telegram ID'''
        user = await User.get_or_none(user_id=user_id).prefetch_related(*cls.prefetch_list)
        if user is None: raise DoesNotExist()
        return user.to_schema()
    
    @classmethod
    async def create(cls, dto: UserCreateDto):
        '''Create user'''
        user = await User.create(
            user_id=dto.user_id,
            email=dto.email,
            full_name=dto.full_name,
            username=dto.username,
        )
