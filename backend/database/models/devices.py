from tortoise import fields, Model

import uuid


class Device(Model):
    id = fields.CharField(pk=True, max_length=20, default=lambda: str(uuid.uuid4().hex)[:12])
    
    title = fields.CharField(max_length=32)
    
    user = fields.ForeignKeyField(
        'models.User',
        related_name='devices',
        to_field='user_id'
    )
    
    register_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'devices'
