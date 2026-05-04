from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse as UserSchema
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByEmailException
import logging

logger = logging.getLogger(__name__)


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, session: AsyncSession, email: str) -> UserSchema:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_email(session=session, email=email)

            except UserNotFoundException:
                error = UserNotFoundByEmailException(email=email)
                logger.error(error.get_detail())
                raise error

            return UserSchema.model_validate(obj=user)
