from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import EmailStr
from typing import List
from core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
    UserLoginOrEmailIsNotUniqueException
)
from schemas.users import UserCreate, UserResponse

from api.depends import (
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    create_user_use_case,
    delete_user_use_case
)

users_router = APIRouter()

@users_router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(use_case = Depends(get_all_users_use_case)) -> List[UserResponse]:
    users = await use_case.execute()
    return users

@users_router.get("/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    use_case = Depends(get_user_by_id_use_case)) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@users_router.get("/login/{login}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_login(
    login: str,
    use_case = Depends(get_user_by_login_use_case)) -> UserResponse:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@users_router.post("/register", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def create_user(
    data: UserCreate,
    use_case = Depends(create_user_use_case)) -> UserResponse:
    try:
        user = await use_case.execute(data=data)
        return user
    except UserLoginOrEmailIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case = Depends(delete_user_use_case)):
    try:
        await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
