from typing import Type, List
from datetime import datetime
from sqlalchemy import select, update
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
    
    async def update_post_image(self, session: AsyncSession, post_id: int, image_path: str) -> Post:
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(image=image_path)
            .returning(self._model)
        )
        
        result = await session.execute(query)
        updated_post = result.scalar_one_or_none()
        
        if not updated_post:
            raise PostNotFoundException()
        
        return updated_post
    
    async def get_post_image(self, session: AsyncSession, post_id: int) -> str:
        query = select(self._model.image).where(self._model.id == post_id)
        result = await session.execute(query)
        image_path = result.scalar_one_or_none()
        if not image_path:
            raise PostNotFoundException("Данный пост не содержит изображения")
        return image_path

    async def create_post(self, session: AsyncSession, data: PostSchema) -> Post:
        author_query = select(self._author_model).where(self._author_model.id == data.author_id)
        author_result = await session.execute(author_query)
        author = author_result.scalar_one_or_none()
        
        if not author:
            raise UserNotFoundException()

        if data.location_id is not None:
            location_query = select(self._location_model).where(self._location_model.id == data.location_id)
            location_result = await session.execute(location_query)
            location = location_result.scalar_one_or_none()
            if not location:
                raise LocationNotFoundException()

        if data.category_id is not None:
            category_query = select(self._category_model).where(self._category_model.id == data.category_id)
            category_result = await session.execute(category_query)
            category = category_result.scalar_one_or_none()
            if not category:
                raise CategoryNotFoundException()

        post_data = data.model_dump(exclude_none=True)
        post = self._model(**post_data)
        session.add(post)
        await session.flush()
        await session.refresh(post)

        return post

    async def delete_post(self, session: AsyncSession, post_id: int) -> None:
        post = await self.get_post_by_id(session, post_id)
        if post:
            await session.delete(post)
            await session.flush()
        else:
            raise PostNotFoundException()
