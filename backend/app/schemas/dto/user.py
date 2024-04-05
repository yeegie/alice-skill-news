from pydantic import BaseModel, EmailStr, validator
from typing import Optional

from models.dataclasses import UserType


class UserCreateDto(BaseModel):
    user_id: int
    email: EmailStr
    full_name: str
    username: str


class UserUpdateDto(BaseModel):
    type: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    username: Optional[str] = None

    @validator('type')
    def validate_type(cls, v):
        UserType.validator(v)
        return v
