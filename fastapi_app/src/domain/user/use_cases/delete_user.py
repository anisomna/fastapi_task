from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByIdException
import logging

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: str) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete_user(session=session, user_id=user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
