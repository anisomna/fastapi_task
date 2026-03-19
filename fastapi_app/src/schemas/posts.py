from pydantic import BaseModel, Field
from datetime import datetime


class Post(BaseModel):
    title: str = Field(..., description='Заголовок', max_length=256)
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(
        description='Дата и время публикации Если установить дату и время в будущем '
        '— можно делать отложенные публикации.')
    is_published: bool = Field(default=True, description='Опубликовано')
    author_id: int = Field(description='Автор публикации')
    location_id: int | None = Field(default=None, description='Местоположение')
    category_id: int | None = Field(default=None, description='Категория')
    image: str | None = Field(default=None, description='URL-ссылка на изображение')
    created_at: datetime = Field(default=None, description='Добавлено')


class PostResponse(Post):
    id: int
