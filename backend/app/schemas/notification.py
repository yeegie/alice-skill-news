from pydantic import BaseModel
from typing import Union, List


class NotificationSchema(BaseModel):
    target: Union[int, List[int]]
    message: str
