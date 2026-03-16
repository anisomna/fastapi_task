from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import EmailStr
from typing import List

from schemas.users import User, UserCreate, UserResponse

from api.depends import (
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    create_user_use_case,
    delete_user_use_case
)

users_router = APIRouter()

@users_router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
async def get_all_users(use_case = Depends(get_all_users_use_case)) -> List[User]:
    users = await use_case.execute()
    return users

@users_router.get("/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    use_case = Depends(get_user_by_id_use_case)) -> UserResponse:
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
    use_case = Depends(get_user_by_login_use_case)) -> UserResponse:
    try:
        user = await use_case.execute(login=login)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@users_router.post("/register", status_code=status.HTTP_200_OK, response_model=User)
async def create_user(
    login: str, email: EmailStr, password: str, 
    first_name: str | None = None, last_name: str | None = None,
    use_case = Depends(create_user_use_case)) -> User:
    user = await use_case.execute(
            login=login,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
    return user

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case = Depends(delete_user_use_case)):
    try:
        result = await use_case.execute(user_id=user_id)
        if result:
            return {"message": "Пользователь успешно удален"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
