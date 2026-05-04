import logging
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, session: AsyncSession, login: str, current_user: UserResponse) -> UserResponse:
        try:
            user = await self._repo.get_user_by_login(session=session, login=login)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {
                    error.get_detail()}"
            )
            raise error

        user = UserResponse.model_validate(obj=user)
        return user
