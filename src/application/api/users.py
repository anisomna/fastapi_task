from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.database import database
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
    UserLoginOrEmailIsNotUniqueException,
    UserHasNoImageException,
    UploadFileIsNotImageException
)
from application.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from application.schemas.users import UserCreate, UserResponse, UserImageResponse
from application.services.auth import AuthService
from application.api.depends import (
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    create_user_use_case,
    delete_user_use_case,
    update_user_use_case,
    get_user_avatar_use_case,
    add_user_avatar_use_case
)

users_router = APIRouter()

async def get_db():
    async with database.session() as session:
        yield session


@users_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse]
)
async def get_all_users(
    use_case = Depends(get_all_users_use_case),
    session: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    users = await use_case.execute(session=session)
    return users


@users_router.get(
    "/id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user_by_id(
    user_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case = Depends(get_user_by_id_use_case),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id, current_user=user, session=session)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@users_router.get(
    "/login/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user_by_login(
    login: str,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: GetUserByLoginUseCase = Depends(get_user_by_login_use_case),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        return await use_case.execute(login=login, current_user=user, session=session)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@users_router.get(
    "/avatar/user/{user_id}", 
    status_code=status.HTTP_200_OK, 
    response_class=FileResponse,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def get_user_image(
    user_id: int,
    use_case = Depends(get_user_avatar_use_case)) -> FileResponse:
    try:
        return await use_case.execute(user_id=user_id)
    except (UserNotFoundByIdException, UserHasNoImageException) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.get_detail()
        )


@users_router.post(
    "/avatar/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserImageResponse,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def add_user_image(
    user_id: int,
    image: UploadFile = File(...),
    use_case = Depends(add_user_avatar_use_case)) -> UserImageResponse:
    try:
        return await use_case.execute(user_id=user_id, image=image)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.get_detail()
        )
    except UploadFileIsNotImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=exc.get_detail()
        )


@users_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(
    data: UserCreate,
    use_case = Depends(create_user_use_case),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        user = await use_case.execute(data=data, session=session)
        return user
    except UserLoginOrEmailIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case = Depends(delete_user_use_case),
    session: AsyncSession = Depends(get_db)
):
    try:
        await use_case.execute(user_id=user_id, current_user=user, session=session)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@users_router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: int,
    data: UserCreate,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case = Depends(update_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id, current_user=user, data=data)
    except UserLoginOrEmailIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
