from typing import Type, List
from sqlalchemy import insert, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from application.infrastructure.postgres.models.users import User
from application.schemas.users import UserCreate as UserSchema
from pydantic import EmailStr
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException
)
from application.resources.auth import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    async def get_all_users(self, session: AsyncSession) -> List[User]:
        query = session.query(self._model)
        users = query.all()

        if not users:
            raise UserNotFoundException()

        return users

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User:
        query = (
            select(self._model)
            .where(self._model.id == user_id)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    async def get_user_by_login(self, session: AsyncSession, login: str) -> User:
        query = (
            select(self._model)
            .where(self._model.login == login)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> User:
        query = (
            select(self._model)
            .where(self._model.email == email)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    async def create_user(self, session: AsyncSession, data: UserSchema) -> User:
        existing_user = session.scalar(
            select(self._model).where(
                or_(self._model.login == data.login,
                    self._model.email == data.email,
                )
            )
        )

        if existing_user is not None:
            if existing_user.login == data.login:
                raise UserLoginAlreadyExistsException()
            elif existing_user.email == data.email:
                raise UserEmailAlreadyExistsException()

        user_data = data.model_dump()
        user_data['password'] = get_password_hash(user_data['password'])

        query = (
            insert(self._model)
            .values(data.model_dump())
            .returning(self._model)
        )
        user = session.scalar(query)

        return user

    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        user = self.get_user_by_id(session, user_id)
        if user:
            session.delete(user)
        else:
            raise UserNotFoundException()
