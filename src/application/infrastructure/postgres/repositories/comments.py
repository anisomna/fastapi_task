from typing import Type, List
from datetime import datetime
from sqlalchemy import insert, select
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
        query = session.query(self._model)
        comments = query.all()

        if not comments:
            raise CommentNotFoundException()

        return comments

    async def get_comment_by_id(self, session: AsyncSession, comment_id: int) -> Comment:
        query = (
            session.query(self._model)
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()

        if not comment:
            raise CommentNotFoundException()

        return comment

    async def get_comments_by_post(self, session: AsyncSession, post_id: int) -> List[Comment]:
        query = (
            session.query(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        comments = query.all()

        if not comments:
            raise CommentNotFoundException()

        return comments

    async def create_comment(self, session: AsyncSession, data: CommentSchema) -> Comment:
        author = session.get(self._author_model, data.author_id)
        if not author:
            raise UserNotFoundException()

        post = session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    async def delete_comment(self, session: AsyncSession, comment_id: int) -> None:
        comment = self.get_comment_by_id(session, comment_id)
        if comment:
            session.delete(comment)
        else:
            raise CommentNotFoundException()
