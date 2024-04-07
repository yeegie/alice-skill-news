from tortoise import fields
from tortoise import Model

import uuid

from schemas.channel import ChannelSchema


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

    
    async def toggle(self):
        self.active = not self.active
        await self.save()


    async def to_schema(self) -> ChannelSchema:
        return ChannelSchema(
            id=self.id,
            title=self.title,
            channel_id=self.channel_id,
            user_id=self.user_id,
            active=self.active,
        )
