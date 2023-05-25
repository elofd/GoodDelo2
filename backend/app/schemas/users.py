"""
Модели для пользователя и токенов
"""
from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, validator, Field


class TokenBase(BaseModel):
    """
    Модель токена
    """
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class UserBase(BaseModel):
    """
    Модель пользователя
    """
    id: int
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    """
    Модель для создания пользователя
    """
    email: EmailStr
    username: str
    password: str


class User(UserBase):
    """
    Модель пользователя с токеном
    """
    token: TokenBase = {}