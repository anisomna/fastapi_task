from typing import Type, List
from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.posts import Post
from infrastructure.sqlite.models.users import User
from infrastructure.sqlite.models.locations import Location
from infrastructure.sqlite.models.categories import Category
from schemas.posts import Post as PostSchema
from core.exceptions.database_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException
)


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category

    def get_all_posts(self, session: Session) -> List[Post]:
        query = session.query(self._model)
        posts = query.all()

        if not posts:
            raise PostNotFoundException()

        return posts

    def get_published_posts(self, session: Session, limit: int = 10) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True)
            .order_by(self._model.pub_date.desc())
            .limit(limit)
        )
        posts = query.all()

        if not posts:
            raise PostNotFoundException()

        return posts

    def get_post_by_id(self, session: Session, post_id: int) -> Post:
        query = (
            session.query(self._model)
            .where(self._model.id == post_id)
        )
        post = query.scalar()

        if not post:
            raise PostNotFoundException()

        return post

    def get_posts_by_author(self, session: Session, author_id: int) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
        )
        posts = query.all()

        if not posts:
            raise PostNotFoundException()

        return posts

    def create_post(self, session: Session, data: PostSchema) -> Post:
        author = session.get(self._author_model, data.author_id)
        if not author:
            raise UserNotFoundException()

        if data.location_id is not None:
            location = session.get(self._location_model, data.location_id)
            if not location:
                raise LocationNotFoundException()

        if data.category_id is not None:
            category = session.get(self._category_model, data.category_id)
            if not category:
                raise CategoryNotFoundException()

        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def delete_post(self, session: Session, post_id: int) -> None:
        post = self.get_post_by_id(session, post_id)
        if post:
            session.delete(post)
        else:
            raise PostNotFoundException()
