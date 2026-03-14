from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.users import User, UserCreate, UserResponse

from api.depends import (
    get_get_user_by_id_use_case,
    get_get_user_by_login_use_case,
    get_create_user_use_case,
    get_delete_user_use_case
)

users_router = APIRouter()


@users_router.get("/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    use_case = Depends(get_get_user_by_id_use_case)) -> UserResponse:
    try:
        user = await use_case.execute(user_id=user_id)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@users_router.get("/login/{login}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_login(
    login: str,
    use_case = Depends(get_get_user_by_login_use_case)) -> UserResponse:
    try:
        user = await use_case.execute(login=login)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@users_router.post("/user", status_code=status.HTTP_200_OK, response_model=User)
async def create_user(
    data: UserCreate,
    use_case = Depends(get_create_user_use_case)) -> User:
    return await use_case.execute(data)

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case = Depends(get_delete_user_use_case)):
    try:
        result = await use_case.execute(user_id=user_id)
        if result:
            return {"message": "Пользователь успешно удален"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
