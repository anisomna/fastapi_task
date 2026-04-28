from typing import Type, List
from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.users import User
from application.infrastructure.postgres.models.locations import Location
from application.infrastructure.postgres.models.categories import Category
from application.schemas.posts import Post as PostSchema
from application.core.exceptions.database_exceptions import (
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

    async def get_all_posts(self, session: AsyncSession) -> List[Post]:
        query = session.query(self._model)
        posts = query.all()

        if not posts:
            raise PostNotFoundException()

        return posts

    async def get_published_posts(self, session: AsyncSession, limit: int = 10) -> List[Post]:
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

    async def get_post_by_id(self, session: AsyncSession, post_id: int) -> Post:
        query = (
            session.query(self._model)
            .where(self._model.id == post_id)
        )
        post = query.scalar()

        if not post:
            raise PostNotFoundException()

        return post

    async def get_posts_by_author(self, session: AsyncSession, author_id: int) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
        )
        posts = query.all()

        if not posts:
            raise PostNotFoundException()

        return posts

    async def create_post(self, session: AsyncSession, data: PostSchema) -> Post:
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

    async def delete_post(self, session: AsyncSession, post_id: int) -> None:
        post = self.get_post_by_id(session, post_id)
        if post:
            session.delete(post)
        else:
            raise PostNotFoundException()
