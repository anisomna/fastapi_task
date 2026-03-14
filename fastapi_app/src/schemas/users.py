from pydantic import BaseModel, SecretStr, Field, EmailStr
from typing import Optional


class User(BaseModel):
    login: str
    email: EmailStr
    first_name: Optional[str] = Field(max_length=30)
    last_name: Optional[str] = Field(max_length=30)


class UserCreate(User):
    password: str = Field(min_length=8)


class UserResponse(User):
    id: int
    login: str
    email: EmailStr
    first_name: str
    last_name: str
