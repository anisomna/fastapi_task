from fastapi import HTTPException, status
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.infrastructure.postgres.models.users import User as UserModel
from application.schemas.users import UserCreate, UserResponse
from pydantic import EmailStr
from application.core.exceptions.database_exceptions import (
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException
)
from application.core.exceptions.domain_exceptions import (
    UserLoginOrEmailIsNotUniqueException
)
from application.resources.auth import get_password_hash
import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserResponse:
        user_data = UserCreate(
            login=data.login,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            password=get_password_hash(data.password)
        )

        async with self._database.session() as session:
            try:
                user = await self._repo.create_user(session=session, data=user_data)
            except UserLoginAlreadyExistsException:
                error = UserLoginOrEmailIsNotUniqueException.from_login(
                    login=data.login
                )
                logger.error(error.get_detail())
                raise error
            except UserEmailAlreadyExistsException:
                error = UserLoginOrEmailIsNotUniqueException.from_email(
                    email=data.email
                )
                logger.error(error.get_detail())
                raise error

            return UserResponse.model_validate(obj=user)