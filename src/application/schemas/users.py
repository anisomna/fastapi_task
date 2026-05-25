from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from fastapi import HTTPException, status


class User(BaseModel):
    login: str
    email: EmailStr
    first_name: str | None = Field(default=None, max_length=30)
    last_name: str | None = Field(default=None, max_length=30)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    password: str

    @field_validator("password", mode="after")
    @staticmethod
    def check_password(password: str) -> str:
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен быть не менее 8 символов"
            )

        return password


class UserResponse(User):
    id: int
    image: str | None = Field(default=None, description='Аватар пользователя')
    model_config = ConfigDict(from_attributes=True)


class UserImageResponse(BaseModel):
    image: str
