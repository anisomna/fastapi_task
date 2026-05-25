import uuid
from typing import Type, List, Optional
from sqlalchemy import select, or_, insert, update
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
    
    async def update_user_avatar(self, session: AsyncSession, user_id: int, image_path: str) -> User:
        query = (
            update(self._model)
            .where(self._model.id == user_id)
            .values(image=image_path)
            .returning(self._model)
        )
        
        result = await session.execute(query)
        updated_user = result.scalar_one_or_none()
        
        if not updated_user:
            raise UserNotFoundException()
        
        return updated_user
    
    async def get_user_avatar(self, session: AsyncSession, user_id: int) -> str:
        user = await self.get_user_by_id(session, user_id)
        image_path = user.scalar_one_or_none()
        if not image_path:
            raise UserNotFoundException("Аватар не установлен")
        return image_path

    async def create_user(self, session: AsyncSession, data: UserSchema) -> User:
        user_dict = data.model_dump()
        user_dict["password"] = get_password_hash(user_dict.pop("password"))
        query = insert(self._model).values(user_dict).returning(self._model)
        try:
            user = await session.scalar(query)
            return user
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "users_login_key" in error_msg:
                raise UserLoginAlreadyExistsException()
            elif "users_email_key" in error_msg:
                raise UserEmailAlreadyExistsException()
            raise
    
    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_user_by_id(session, user_id)
        if user:
            await session.delete(user)
            await session.flush()
        else:
            raise UserNotFoundException()

    async def update_user(self, session: AsyncSession, user_id: int, data: UserSchema) -> User:
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data.pop("password"))
        query = (
            update(self._model)
            .where(self._model.id == user_id)
            .values(update_data)
            .returning(self._model)
        )
        try:
            user = await session.scalar(query)
            if not user:
                raise UserNotFoundException()
            return user
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "users_login_key" in error_msg:
                raise UserLoginAlreadyExistsException()
            if "users_email_key" in error_msg:
                raise UserEmailAlreadyExistsException()
            raise
