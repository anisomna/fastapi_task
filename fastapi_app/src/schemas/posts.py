from pydantic import BaseModel, Field
from datetime import datetime
from schemas.users import User
from schemas.locations import Location
from schemas.categories import Category


class Post(BaseModel):
    title: str = Field(..., description='Заголовок', max_length=256)
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(
        description='Дата и время публикации Если установить дату и время в будущем '
        '— можно делать отложенные публикации.')
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Добавлено')
    author: User = Field(description='Автор публикации')
    location: Location = Field(default=None, description='Местоположение')
    category: Category = Field(default=None, description='Категория')
    image: str = Field(default=None, description='URL-ссылка на изображение')
