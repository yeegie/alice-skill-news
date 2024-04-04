from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateDto(BaseModel):
    user_id: int
    email: EmailStr
    full_name: str
    username: str


class UserUpdateDto(BaseModel):
    type: str
    email: EmailStr
    full_name: str
    username: Optional[str] = None
