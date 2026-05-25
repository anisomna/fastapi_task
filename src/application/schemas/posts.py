from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


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
    created_at: datetime = Field(default=None, description='Добавлено')


class PostResponse(Post):
    id: int
    images: List[str] = Field(default_factory=list, description="Список изображений")
    model_config = ConfigDict(from_attributes=True)


class PostImageResponse(BaseModel):
    image: str
