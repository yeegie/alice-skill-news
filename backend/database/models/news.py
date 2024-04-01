from tortoise import Model, fields


class News(Model):
    id = fields.IntField(pk=True)
    last_update = fields.DatetimeField(auto_now=True)
    last_news = fields.JSONField(null=True, default=[])
    user = fields.ForeignKeyField(
        'models.User',
        related_name='news',
    )

    class Meta:
        table = 'news'

    @property
    def clear_news(self):
        self.last_news = []
