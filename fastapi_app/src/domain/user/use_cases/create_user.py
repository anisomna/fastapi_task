from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from infrastructure.sqlite.models.users import User as UserModel
from schemas.users import UserCreate
from pydantic import EmailStr


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, login: str, email: EmailStr,  password: str, 
        first_name: str | None = None, last_name: str | None = None) -> UserCreate:
        with self._database.session() as session:
            existing_login = self._repo.get_user_by_login(session, login)
            existing_email = self._repo.get_user_by_email(session, email)
            if existing_login:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь с таким логином уже существует"
                )
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь с такой почтой уже существует"
                )

            user = self._repo.create_user(
                session=session,
                login=login,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            user_dict = {
                "login": user.login,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "password": user.password
            }

            return UserCreate.model_validate(obj=user_dict)
