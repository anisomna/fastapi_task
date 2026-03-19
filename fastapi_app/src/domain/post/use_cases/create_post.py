from datetime import datetime
from fastapi import HTTPException
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.users import UserRepository
from infrastructure.sqlite.repositories.locations import LocationRepository
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.posts import Post as PostSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(
        self, title: str, text: str,
        pub_date: datetime, author_id: int,
        location_id: int | None = None,
        category_id: int | None = None,
        image: str | None = None,
        is_published: bool = True) -> PostSchema:
        with self._database.session() as session:
            author = self._user_repo.get_user_by_id(session, author_id)
            location = self._location_repo.get_location_by_id(session, location_id)
            category = self._category_repo.get_category_by_id(session, category_id)

            if not author:
                raise ValueError(f"Автор с id {author_id} не найден")

            if not location:
                raise ValueError(f"Локация с id {location_id} не найдена")
            
            if not category:
                raise ValueError(f"Категория с id {category_id} не найдена")

            post = self._repo.create_post(
                session=session,
                title=title,
                text=text,
                pub_date=pub_date,
                author_id=author_id,
                location_id=location_id,
                category_id=category_id,
                image=image,
                is_published=is_published
            )

            post_dict = {
                "id": post.id,
                "title": post.title,
                "text": post.text,
                "pub_date": post.pub_date,
                "created_at": post.created_at,
                "author_id": post.author_id,
                "location_id": post.location_id,
                "category_id": post.category_id,
                "image": post.image,
                "is_published": post.is_published
            }

            return PostSchema.model_validate(obj=post_dict)
