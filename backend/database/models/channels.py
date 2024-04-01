from tortoise import fields
from tortoise import Model

import uuid


class Channel(Model):
    id = fields.CharField(pk=True, max_length=20, default=lambda: str(uuid.uuid4().hex)[:12])

    title = fields.CharField(max_length=32)
    channel_id = fields.CharField(max_length=32, unique=True)

    user = fields.ForeignKeyField(
        'models.User',
        related_name='channels',
        to_field='user_id'
    )
    
    active = fields.BooleanField(default=True)

    class Meta:
        table = 'channels'
