from typing import Type, List
from datetime import datetime
from sqlalchemy import select, update, insert
from sqlalchemy.exc import IntegrityError
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
        query = select(self._model)
        result = await session.execute(query)
        posts = result.scalars().all()

        if not posts:
            raise PostNotFoundException()

        return posts

    async def get_published_posts(self, session: AsyncSession, limit: int = 10) -> List[Post]:
        query = (
            select(self._model)
            .where(self._model.is_published == True)
            .order_by(self._model.pub_date.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        posts = result.scalars().all()

        if not posts:
            raise PostNotFoundException()

        return posts

    async def get_post_by_id(self, session: AsyncSession, post_id: int) -> Post:
        query = select(self._model).where(self._model.id == post_id)
        result = await session.execute(query)
        post = result.scalar_one_or_none()

        if not post:
            raise PostNotFoundException()

        return post

    async def get_posts_by_author(self, session: AsyncSession, author_id: int) -> List[Post]:
        query = select(self._model).where(self._model.author_id == author_id)
        result = await session.execute(query)
        posts = result.scalars().all()

        if not posts:
            raise PostNotFoundException()

        return posts
    
    async def add_post_images(
        self, session: AsyncSession, post_id: int, image_paths: list
    ) -> Post:
        post = await self.get_post_by_id(session, post_id)
        current_images = post.images or []
        current_images.extend(image_paths)
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(images=current_images)
            .returning(self._model)
        )
        updated_post = await session.scalar(query)
        if not updated_post:
            raise PostNotFoundException()
        return updated_post

    async def update_post_images(
        self, session: AsyncSession, post_id: int, image_path: list
    ) -> Post:
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(images=image_path)
            .returning(self._model)
        )
        result = await session.scalar(query)
        if not result:
            raise PostNotFoundException()
        return result

    async def get_post_images(self, session: AsyncSession, post_id: int) -> list:
        post = await self.get_post_by_id(session, post_id)
        return post.images

    async def create_post(self, session: AsyncSession, data: PostSchema) -> Post:
        post_data = data.model_dump(exclude_none=True)
        query = insert(self._model).values(post_data).returning(self._model)
        try:
            post = await session.scalar(query)
            return post
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "posts_author_id_fkey" in error_msg:
                raise UserNotFoundException()
            elif "posts_location_id_fkey" in error_msg:
                raise LocationNotFoundException()
            elif "posts_category_id_fkey" in error_msg:
                raise CategoryNotFoundException()
            raise

    async def delete_post(self, session: AsyncSession, post_id: int) -> None:
        post = await self.get_post_by_id(session, post_id)
        if post:
            await session.delete(post)
            await session.flush()
        else:
            raise PostNotFoundException()
