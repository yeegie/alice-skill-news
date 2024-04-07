from aiogram import Bot
from data.config import Telegram
from models.schemas.notification import NotificationSchema
from aiohttp.web import Request, Response

from loguru import logger


async def notification_handler(request: Request) -> Response:
    try:
        data = await request.json()
        notification = NotificationSchema(
            target=data['target'],
            message=data['message'],
        )
    except Exception as ex:
        logger.error(str(ex))
        
    bot = Bot(Telegram.token)
    
    if notification.target is list:
        for target in notification.target:
            await bot.send_message(target, notification.message)
    else:
        await bot.send_message(notification.target, notification.message)

    return Response(status=204)