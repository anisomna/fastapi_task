from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile
from typing import List
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException,
    UploadFileIsNotImageException,
)
from application.schemas.posts import PostImageResponse, PostResponse, Post
from application.services.auth import AuthService
from application.api.depends import (
    get_all_posts_use_case,
    get_post_by_id_use_case,
    create_post_use_case,
    delete_post_use_case,
    get_post_images_use_case,
    add_post_image_use_case
)

posts_router = APIRouter()

@posts_router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def get_all_posts(use_case = Depends(get_all_posts_use_case)) -> List[PostResponse]:
    posts = await use_case.execute()
    return posts


@posts_router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_post_by_id(
    post_id: int,
    use_case = Depends(get_post_by_id_use_case)) -> PostResponse:
    try:
        post = await use_case.execute(post_id=post_id)
        return post
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@posts_router.post(
    "/{post_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=PostImageResponse,
    dependencies=[Depends(AuthService.get_current_user)],
)
async def add_post_image(
    post_id: int,
    image: UploadFile = File(...), 
    use_case = Depends(add_post_image_use_case),) -> PostImageResponse:
    try:
        return await use_case.execute(post_id=post_id, image=image)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.get_detail()
        )
    except UploadFileIsNotImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=exc.get_detail()
        )

@posts_router.get(
    "/{post_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=List[PostImageResponse],
)
async def get_post_images(
    post_id: int,
    use_case=Depends(get_post_images_use_case)) -> List[PostImageResponse]:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@posts_router.post(
    "/create_post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def create_post(
    data: Post,
    use_case = Depends(create_post_use_case)) -> PostResponse:
    try:
        post = await use_case.execute(data=data)
        return post
    except (
        UserNotFoundByIdException,
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@posts_router.delete(
    "/delete/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def delete_post(
    post_id: int,
    use_case = Depends(delete_post_use_case)):
    try:
        await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
