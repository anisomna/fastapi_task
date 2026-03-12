from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime

from schemas.locations import Location

from api.depends import (
    get_get_all_locations_use_case,
    get_get_location_by_id_use_case,
    get_create_location_use_case,
    get_delete_location_use_case
)

locations_router = APIRouter()

locations = []
next_id = 1

@locations_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Location])
async def get_all_locations(use_case = Depends(get_get_all_locations_use_case)) -> List[Location]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/{location_id}", status_code=status.HTTP_200_OK, response_model=Location)
async def get_location_by_id(
    location_id: int,
    use_case = Depends(get_get_location_by_id_use_case)) -> Location:
    try:
        location = await use_case.execute(location_id=location_id)
        return location
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация не найдена"
        )


@locations_router.location("/add_location", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    name: str, is_published: bool,
    use_case = Depends(get_create_location_use_case)) -> Location:
    try:
        location = await use_case.execute(
            name=name,
            is_published=is_published,
            created_at=datetime.now()
        )
        return location
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@locations_router.delete("/delete/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    use_case = Depends(get_delete_location_use_case)):
    try:
        await use_case.execute(location_id=location_id)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
