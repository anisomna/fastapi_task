from pydantic import BaseModel, SecretStr, Field, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    login: str
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    password: SecretStr
