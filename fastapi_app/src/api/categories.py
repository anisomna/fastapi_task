from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime

from schemas.categories import Category

from api.depends import (
    get_get_all_categories_use_case,
    get_get_category_by_id_use_case,
    get_create_category_use_case,
    get_delete_category_use_case
)

categories_router = APIRouter()

@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Category])
async def get_all_categories(use_case = Depends(get_get_all_categories_use_case)) -> List[Category]:
    categories = await use_case.execute()
    return categories


@categories_router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_by_id(
    category_id: int,
    use_case = Depends(get_get_category_by_id_use_case)) -> Category:
    try:
        category = await use_case.execute(category_id=category_id)
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
