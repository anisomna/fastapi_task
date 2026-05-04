from application.infrastructure.postgres.repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from application.schemas.users import UserCreate, UserResponse
from application.infrastructure.postgres.database import database
from application.core.exceptions.database_exceptions import UserEmailAlreadyExistsException, UserLoginAlreadyExistsException
from application.core.exceptions.domain_exceptions import UserLoginOrEmailIsNotUniqueException


import logging
logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, session: AsyncSession, data: UserCreate) -> UserResponse:
        repo = UserRepository()

        try:
            user = await repo.create_user(session=session, data=data)

            await session.commit()

            logger.info(f"User {user.login} has been created")
            return UserResponse.model_validate(user)
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