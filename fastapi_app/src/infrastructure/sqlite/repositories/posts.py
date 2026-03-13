from typing import Type, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.posts import Post


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_all_posts(self, session: Session) -> List[Post]:
        query = session.query(self._model)
        return query.all()

    def get_published_posts(self, session: Session, limit: int = 10) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True)
            .order_by(self._model.pub_date.desc())
            .limit(limit)
        )
        return query.all()

    def get_post_by_id(self, session: Session, post_id: int) -> Post:
        query = (
            session.query(self._model)
            .where(self._model.id == post_id)
        )
        return query.scalar()

    def get_posts_by_author(self, session: Session, author_id: int) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
        )
        return query.all()

    def create_post(self, session: Session, title: str, text: str,
                   pub_date: datetime, author_id: int,
                   location_id: int | None = None,
                   category_id: int | None = None,
                   image: int | None = None,
                   is_published: bool = True) -> Post:
        post = Post(
            title=title,
            text=text,
            author_id=author_id,
            location_id=location_id,
            category_id=category_id,
            image=image,
            pub_date=pub_date,
            is_published=is_published,
            created_at=datetime.now()
        )
        session.add(post)
        session.flush()
        return post

    def delete_post(self, session: Session, post_id: int) -> bool:
        post = self.get_post_by_id(session, post_id)
        if post:
            session.delete(post)
            return True
        return False
