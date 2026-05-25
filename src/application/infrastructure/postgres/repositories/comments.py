from typing import Type, List
from sqlalchemy import select, update, insert
from sqlalchemy.exc import IntegrityError
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
    
    async def add_comment_images(self, session: AsyncSession, comment_id: int, image_paths: list) -> Comment:
        comment = await self.get_comment_by_id(session, comment_id)
        current_images = comment.images or []
        current_images.extend(image_paths)
        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(images=current_images)
            .returning(self._model)
        )
        updated_comment = await session.scalar(query)
        if not updated_comment:
            raise CommentNotFoundException()
        return updated_comment
    
    async def update_comment_images(
        self, session: AsyncSession, comment_id: int, image_path: list
    ) -> Comment:
        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(images=image_path)
            .returning(self._model)
        )
        result = await session.scalar(query)
        if not result:
            raise CommentNotFoundException()
        return result

    async def get_comment_images(self, session: AsyncSession, comment_id: int) -> list:
        comment = await self.get_comment_by_id(session, comment_id)
        return comment.images

    async def create_comment(
        self, session: AsyncSession, data: CommentSchema
    ) -> Comment:
        comment_dict = data.model_dump(exclude_none=True)
        query = insert(self._model).values(comment_dict).returning(self._model)
        try:
            comment = await session.scalar(query)
            return comment
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "fk_comments_author_id" in error_msg:
                raise UserNotFoundException()
            elif "fk_comments_post_id" in error_msg:
                raise PostNotFoundException()
            raise

    async def delete_comment(self, session: AsyncSession, comment_id: int) -> None:
        comment = await self.get_comment_by_id(session, comment_id)
        if comment:
            await session.delete(comment)
            await session.flush()
        else:
            raise CommentNotFoundException()
