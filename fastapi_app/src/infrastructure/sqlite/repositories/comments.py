from typing import Type, List
from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.comments import Comment
from infrastructure.sqlite.models.users import User
from infrastructure.sqlite.models.posts import Post
from schemas.comments import Comment as CommentSchema
from core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException
)


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._author_model: Type[User] = User
        self._post_model: Type[Post] = Post

    def get_all_comments(self, session: Session) -> List[Comment]:
        query = session.query(self._model)
        comments = query.all()

        if not comments:
            raise CommentNotFoundException()

        return comments

    def get_comment_by_id(self, session: Session, comment_id: int) -> Comment:
        query = (
            session.query(self._model)
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()

        if not comment:
            raise CommentNotFoundException()

        return comment

    def get_comments_by_post(self, session: Session, post_id: int) -> List[Comment]:
        query = (
            session.query(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        comments = query.all()

        if not comments:
            raise CommentNotFoundException()

        return comments

    def create_comment(self, session: Session, data: CommentSchema) -> Comment:
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

    def delete_comment(self, session: Session, comment_id: int) -> None:
        comment = self.get_comment_by_id(session, comment_id)
        if comment:
            session.delete(comment)
        else:
            raise CommentNotFoundException()