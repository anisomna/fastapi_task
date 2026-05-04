import uuid
from typing import Type, List, Optional
from sqlalchemy import select, or_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from application.infrastructure.postgres.models.users import User
from application.schemas.users import UserCreate as UserSchema
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException
)
from application.resources.auth import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    async def get_all_users(self, session: AsyncSession) -> List[User]:
        query = select(self._model)
        result = await session.execute(query)
        users = result.scalars().all()

        if not users:
            raise UserNotFoundException()

        return users

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User:
        query = select(self._model).where(self._model.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFoundException()

        return user

    async def get_user_by_login(self, session: AsyncSession, login: str) -> User:
        query = select(self._model).where(self._model.login == login)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFoundException()

        return user
    
    async def get_user_by_email(self, session: AsyncSession, email: EmailStr) -> User:
        query = select(self._model).where(self._model.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFoundException()

        return user
    
    async def create_user(self, session: AsyncSession, data: UserSchema) -> User:
        query = select(self._model).where(
            or_(
                self._model.login == data.login,
                self._model.email == data.email,
            )
        )
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            if existing_user.login == data.login:
                raise UserLoginAlreadyExistsException()
            elif existing_user.email == data.email:
                raise UserEmailAlreadyExistsException()

        user_data = data.model_dump()
        user_data['password'] = get_password_hash(user_data['password'])

        user = self._model(**user_data)
        session.add(user)
        await session.flush()
        await session.refresh(user)
        
        return user

    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_user_by_id(session, user_id)
        if user:
            await session.delete(user)
            await session.flush()
        else:
            raise UserNotFoundException()
        