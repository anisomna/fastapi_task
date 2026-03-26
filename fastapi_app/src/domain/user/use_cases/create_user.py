from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from infrastructure.sqlite.models.users import User as UserModel
from schemas.users import UserCreate, UserResponse
from pydantic import EmailStr
from core.exceptions.database_exceptions import (
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException
)
from core.exceptions.domain_exceptions import (
    UserLoginOrEmailIsNotUniqueException
)
import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.create_user(session=session, data=data)
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
