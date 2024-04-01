from typing import Any, Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from services.user_service import UserService


# class IsAuth(BaseFilter):
#     async def __call__(
#         self,
#         event: Union[Message, CallbackQuery],
#     ) -> bool:
#         if await UserService.check(event.message.from_user.id):
