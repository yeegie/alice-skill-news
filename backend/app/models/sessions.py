from tortoise import fields
from tortoise import Model

import uuid

from schemas.session import SessionSchema


class Session(Model):
    id = fields.CharField(pk=True, max_length=20, default=lambda: str(uuid.uuid4().hex)[:12])

    secret = fields.CharField(unique=True, max_length=64)

    start_time = fields.DatetimeField(auto_now_add=True)
    end_time = fields.DatetimeField()

    user = fields.ForeignKeyField(
        'models.User',
        related_name='sessions',
        to_field='user_id'
    )

    active = fields.BooleanField(default=True)

    class Meta:
        table = 'sessions'

    def to_schema(self) -> SessionSchema:
        return SessionSchema(
            id=self.id,
            secret=self.secret,
            start_time=self.start_time,
            end_time=self.end_time,
            user_id=self.user_id,
            active=self.active,
        )
