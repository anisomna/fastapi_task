from pydantic import BaseModel, Field
from datetime import datetime


class Category(BaseModel):
    id: int
    title: str = Field(..., description='Заголовок', max_length=256)
    description: str = Field(description='Описание')
    slug: str = Field(..., description='Идентификатор страницы для URL')
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Добавлено')
