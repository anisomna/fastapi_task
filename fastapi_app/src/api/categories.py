from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugIsNotUniqueException
)
from schemas.categories import CategoryRespons, Category

from api.depends import (
    get_all_categories_use_case,
    get_category_by_id_use_case,
    create_category_use_case,
    delete_category_use_case
)

categories_router = APIRouter()

@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
async def get_all_categories(use_case = Depends(get_all_categories_use_case)) -> List[CategoryResponse]:
    categories = await use_case.execute()
    return categories


@categories_router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    use_case = Depends(get_category_by_id_use_case)) -> CategoryResponse:
    try:
        category = await use_case.execute(category_id=category_id)
        return category
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

@categories_router.post("/add_category", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(
    data: Category,
    use_case = Depends(create_category_use_case)) -> CategoryResponse:
    try:
        category = await use_case.execute(data=data)
        return category
    except CategorySlugIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@categories_router.delete("/delete/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case = Depends(delete_category_use_case)):
    try:
        category = await use_case.execute(category_id=category_id)
        return category
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
