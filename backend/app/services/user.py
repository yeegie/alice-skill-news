from models import User
from schemas.user import UserSchema
from schemas.dto.user import UserCreateDto, UserUpdateDto

from tortoise.exceptions import DoesNotExist


class UserService():
    prefetch_list = ['sessions', 'channels', 'news']

    @classmethod
    async def get_user(cls, id: str) -> UserSchema:
        '''Get user by uuid'''
        user = await User.get_or_none(id=id)
        if user is None: raise DoesNotExist()
        return user.to_schema()

    
    @classmethod
    async def get_user_by_user_id(cls, user_id: int) -> UserSchema:
        '''Get user by unique Telegram ID'''
        user = await User.get_or_none(user_id=user_id)
        if user is None: raise DoesNotExist()
        return user.to_schema()
