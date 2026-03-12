from infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .categories import Category
from .comments import Comment
from .users import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    title: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )
    pub_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    image: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    author: Mapped["User"] = relationship(back_populates="posts")
    location: Mapped["Location"] = relationship(back_populates="posts")
    category: Mapped["Category"] = relationship(back_populates="posts")
    comments: Mapped["Comment"] = relationship(back_populates="posts")
