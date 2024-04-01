from tortoise import fields
from tortoise import Model
from .dataclasses import UserType

import uuid


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
