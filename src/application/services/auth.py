from typing import Annotated
from fastapi import Depends
from jose import JWTError, jwt

from application.core.exceptions.auth_exceptions import CredentialsException
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.schemas.users import UserResponse
from application.resources.auth import oauth2_scheme
from application.infrastructure.postgres.database import database, PostgresDatabase
from application.infrastructure.postgres.repositories.users import UserRepository
from application.core.config import settings

class AuthService:
    @staticmethod
    async def _resolve_user_from_token(token: str) -> UserResponse:
        _AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
        _database: PostgresDatabase = database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[settings.AUTH_ALGORITHM],
            )
            login = payload.get('sub')
            if login is None:
                raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail="Токен недействителен или истек")

        try:
            async with _database.session() as session:
                user = await _repo.get_user_by_login(session=session, login=login)
        except UserNotFoundException:
            raise CredentialsException(detail="Пользователь не найден")

        return UserResponse.model_validate(obj=user)

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserResponse:
        return await AuthService._resolve_user_from_token(token=token)
