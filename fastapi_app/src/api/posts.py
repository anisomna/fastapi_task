from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime

from schemas.posts import Post

from api.depends import (
    get_get_all_posts_use_case,
    get_get_post_by_id_use_case,
    get_create_post_use_case,
    get_delete_post_use_case
)

posts_router = APIRouter()

@posts_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_all_posts(use_case = Depends(get_get_all_posts_use_case)) -> List[Post]:
    posts = await use_case.execute()
    return posts


@posts_router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def get_post_by_id(
    post_id: int,
    use_case = Depends(get_get_post_by_id_use_case)) -> Post:
    try:
        post = await use_case.execute(post_id=post_id)
        return post
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@posts_router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    title: str, text: str,
    pub_date: datetime, author_id: int,
    is_published: bool = True,
    location_id: int | None = None,
    category_id: int | None = None,
    image: str | None = None,
    use_case = Depends(get_create_post_use_case)) -> Post:
    try:
        post = await use_case.execute(
            title=title,
            text=text,
            pub_date=pub_date,
            is_published=is_published,
            author_id=author_id,
            location_id=location_id,
            category_id=category_id,
            image=image
        )
        return post
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@posts_router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    use_case = Depends(get_delete_post_use_case)):
    try:
        await use_case.execute(post_id=post_id)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
