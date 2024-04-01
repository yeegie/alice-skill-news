from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from typing import Union, Any, Dict, Callable, Awaitable

class ManageUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        
        return await handler(event, data)