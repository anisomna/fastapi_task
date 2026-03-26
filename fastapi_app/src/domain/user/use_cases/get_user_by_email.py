from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse as UserSchema
from fastapi import HTTPException, status
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByEmailException
import logging

logger = logging.getLogger(__name__)


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str) -> UserSchema:
        with self._database.session() as session:
            try:
                user = self._repo.get_user_by_email(session, email)

            except UserNotFoundException:
                error = UserNotFoundByEmailException(email=email)
                logger.error(error.get_detail())
                raise error

            return UserSchema.model_validate(obj=user)
