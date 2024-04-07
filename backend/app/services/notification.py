from schemas.notification import NotificationSchema
from backend.config import Bot
import aiohttp
from loguru import logger


class NotificationService:
    @staticmethod
    async def send(data: NotificationSchema):
        header = {
            "Content-Type": "application/json"
        }

        data = {
            "target": data.target,
            "message": data.message,
        }

        async with aiohttp.ClientSession(headers=header) as session:
            response = await session.post(url=Bot.url + '/notification', json=data)

            if response.status != 204:
                logger.error(f'[{response.start}] Notification send error\n{await response.json()}')
