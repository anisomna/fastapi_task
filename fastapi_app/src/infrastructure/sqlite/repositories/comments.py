from typing import Type, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.comments import Comment


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get_comment_by_id(self, session: Session, comment_id: int) -> Comment:
        return session.get(self._model, comment_id)

    def get_comments_by_post(self, session: Session, post_id: int) -> List[Comment]:
        query = (
            session.query(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        return query.all()

    def create(self, session: Session, text: str, author_id: int, post_id: int) -> Comment:
        comment = Comment(
            text=text,
            author_id=author_id,
            post_id=post_id,
            created_at=datetime.now()
        )
        session.add(comment)
        session.flush() # Получить ID без коммита
        return comment

    def delete(self, session: Session, comment_id: int) -> bool:
        comment = self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            return True
        return False
