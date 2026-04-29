from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByIdException
from application.schemas.users import UserResponse
import logging

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: str, current_user: UserResponse) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete_user(session=session, user_id=user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                logger.error(
                    f"Пользователь {current_user.login} довел приложение до ошибки: {error.get_detail()}"
                )
                raise error
