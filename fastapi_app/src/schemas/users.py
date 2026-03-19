from pydantic import BaseModel, SecretStr, Field, EmailStr


class User(BaseModel):
    login: str
    email: EmailStr
    first_name: str | None = Field(max_length=30)
    last_name: str | None = Field(max_length=30)


class UserCreate(User):
    password: str = Field(min_length=8)


class UserResponse(User):
    id: int
    login: str
    email: EmailStr
    first_name: str
    last_name: str
