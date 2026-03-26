from typing import Type, List
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from infrastructure.sqlite.models.users import User
from schemas.users import UserCreate as UserSchema
from pydantic import EmailStr
from core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException
)


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_all_users(self, session: Session) -> List[User]:
        query = session.query(self._model)
        users = query.all()

        if not users:
            raise UserNotFoundException()

        return users

    def get_user_by_id(self, session: Session, user_id: int) -> User:
        query = (
            select(self._model)
            .where(self._model.id == user_id)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def get_user_by_login(self, session: Session, login: str) -> User:
        query = (
            select(self._model)
            .where(self._model.login == login)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user
    
    def get_user_by_email(self, session: Session, email: str) -> User:
        query = (
            select(self._model)
            .where(self._model.email == email)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def create_user(self, session: Session, UserSchema) -> User:
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

        query = (
            insert(self._model)
            .values(data.model_dump())
            .returning(self._model)
        )
        user = session.scalar(query)

        return user

    def delete_user(self, session: Session, user_id: int) -> None:
        user = self.get_user_by_id(session, user_id)
        if user:
            session.delete(user)
        else:
            raise UserNotFoundException()
