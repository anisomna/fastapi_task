from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime
from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.schemas.comments import CommentResponse, Comment
from application.services.auth import AuthService
from application.api.depends import (
    get_all_comments_use_case,
    get_comment_by_id_use_case,
    create_comment_use_case,
    delete_comment_use_case
)

comments_router = APIRouter()

@comments_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
async def get_all_comments(use_case = Depends(get_all_comments_use_case)) -> List[CommentResponse]:
    comments = await use_case.execute()
    return comments


@comments_router.get("/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse)
async def get_comment_by_id(
    comment_id: int,
    use_case = Depends(get_comment_by_id_use_case)) -> CommentResponse:
    try:
        comment = await use_case.execute(comment_id=comment_id)
        return comment
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@comments_router.post(
    "/create_comment", 
    status_code=status.HTTP_201_CREATED, 
    response_model=CommentResponse,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def create_comment(
    data: Comment,
    use_case = Depends(create_comment_use_case)) -> CommentResponse:
    try:
        comment = await use_case.execute(data=data)
        return comment
    except (UserNotFoundByIdException, PostNotFoundByIdException) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@comments_router.delete(
    "/delete/{comment_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def delete_comment(
    comment_id: int,
    use_case = Depends(delete_comment_use_case)):
    try:
        await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
