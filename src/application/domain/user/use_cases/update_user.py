import logging
from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException,
)
from application.core.exceptions.domain_exceptions import UserLoginOrEmailIsNotUniqueException
from application.schemas.users import UserCreate, UserResponse
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user: UserResponse, data: UserCreate) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.update_user(
                    session=session, user_id=user_id, user_data=data
                )
                await session.commit()
                await session.refresh(user)
            except UserLoginAlreadyExistsException:
                error = UserLoginOrEmailIsNotUniqueException.from_login(
                    login=data.login
                )
                logger.error(error.get_detail())
                logger.error(
                    f"Пользователь {current_user.login} довел приложение до ошибки: {error.get_detail()}"
                )
                raise error
            except UserEmailAlreadyExistsException:
                error = UserLoginOrEmailIsNotUniqueException.from_email(
                    email=data.email
                )
                logger.error(error.get_detail())
                logger.error(
                    f"Пользователь {current_user.login} довел приложение до ошибки: {error.get_detail()}"
                )
                raise error
            return UserResponse.model_validate(obj=user)
