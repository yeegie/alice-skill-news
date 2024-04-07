from tortoise import fields
from tortoise import Model
from .dataclasses import UserType
from schemas.user import UserSchema

import uuid
import json


class User(Model):
    id = fields.CharField(pk=True, max_length=20, default=lambda: str(uuid.uuid4().hex)[:12])

    type = fields.CharField(max_length=32, default=UserType.user, validators=[UserType.validator])
    
    user_id = fields.BigIntField(unique=True)  # telegram user_id
    yandex_id = fields.CharField(max_length=64, null=True)  # session.user.user_id
    
    full_name = fields.CharField(max_length=64)
    username = fields.CharField(max_length=32, null=True)
    
    email = fields.CharField(max_length=64, unique=True)
    
    register_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'users'

    @property
    def is_admin(self) -> bool:
        return self.type == UserType.admin
    
    async def to_schema(self) -> UserSchema:
        '''Make tortoise model to -> UserSchema'''
        return UserSchema(
            id=self.id,
            type=self.type,
            user_id=self.user_id,
            yandex_id=self.yandex_id,
            full_name=self.full_name,
            username=self.username,
            email=self.email,
            register_time=self.register_time,
            sessions=[await session.to_schema() for session in await self.sessions.all()],
            channels=[await channel.to_schema() for channel in await self.channels.all()],
            news=self.news,
        )
    
    async def to_json(self):
        '''Make tortoise model to -> dict'''
        data = UserSchema(
            id=self.id,
            type=self.type,
            user_id=self.user_id,
            yandex_id=self.yandex_id,
            full_name=self.full_name,
            username=self.username,
            email=self.email,
            register_time=self.register_time,
            sessions=[await session.to_schema() for session in await self.sessions.all()],
            channels=[await channel.to_schema() for channel in await self.channels.all()],
            news=self.news,
        ).model_dump(mode='json')

        return data
