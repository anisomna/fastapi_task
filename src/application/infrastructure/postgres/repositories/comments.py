from typing import Type, List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.models.comments import Comment
from application.infrastructure.postgres.models.users import User
from application.infrastructure.postgres.models.posts import Post
from application.schemas.comments import Comment as CommentSchema
from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException
)


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._author_model: Type[User] = User
        self._post_model: Type[Post] = Post

    async def get_all_comments(self, session: AsyncSession) -> List[Comment]:
        query = select(self._model)
        result = await session.execute(query)
        comments = result.scalars().all()

        if not comments:
            raise CommentNotFoundException()

        return comments

    async def get_comment_by_id(self, session: AsyncSession, comment_id: int) -> Comment:
        query = select(self._model).where(self._model.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()

        if not comment:
            raise CommentNotFoundException()

        return comment

    async def get_comments_by_post(self, session: AsyncSession, post_id: int) -> List[Comment]:
        query = (
            select(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        result = await session.execute(query)
        comments = result.scalars().all()

        if not comments:
            raise CommentNotFoundException()

        return comments

    async def create_comment(self, session: AsyncSession, data: CommentSchema) -> Comment:
        author_query = select(self._author_model).where(self._author_model.id == data.author_id)
        author_result = await session.execute(author_query)
        author = author_result.scalar_one_or_none()
        
        if not author:
            raise UserNotFoundException()

        # Check if post exists
        post_query = select(self._post_model).where(self._post_model.id == data.post_id)
        post_result = await session.execute(post_query)
        post = post_result.scalar_one_or_none()
        
        if not post:
            raise PostNotFoundException()

        comment_data = data.model_dump(exclude_none=True)
        comment = self._model(**comment_data)
        session.add(comment)
        await session.flush()
        await session.refresh(comment)

        return comment

    async def delete_comment(self, session: AsyncSession, comment_id: int) -> None:
        comment = await self.get_comment_by_id(session, comment_id)
        if comment:
            await session.delete(comment)
            await session.flush()
        else:
            raise CommentNotFoundException()
