from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime

from schemas.comments import Comment

from api.depends import (
    get_all_comments_use_case,
    get_comment_by_id_use_case,
    create_comment_use_case,
    delete_comment_use_case
)

comments_router = APIRouter()

@comments_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Comment])
async def get_all_comments(use_case = Depends(get_all_comments_use_case)) -> List[Comment]:
    comments = await use_case.execute()
    return comments


@comments_router.get("/{comment_id}", status_code=status.HTTP_200_OK, response_model=Comment)
async def get_comment_by_id(
    comment_id: int,
    use_case = Depends(get_comment_by_id_use_case)) -> Comment:
    try:
        comment = await use_case.execute(comment_id=comment_id)
        return comment
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@comments_router.post("/create_comment", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    text: str, post_id: int, author_id: int,
    use_case = Depends(create_comment_use_case)) -> Comment:
    try:
        comment = await use_case.execute(
            text=text,
            post_id=post_id,
            author_id=author_id
        )
        return comment
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@comments_router.delete("/delete/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    use_case = Depends(delete_comment_use_case)):
    try:
        await use_case.execute(comment_id=comment_id)
        return
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
