from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime
from core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
    LocationNameIsNotUniqueException
)
from schemas.locations import LocationResponse, Location
from services.auth import AuthService
from api.depends import (
    get_all_locations_use_case,
    get_location_by_id_use_case,
    create_location_use_case,
    delete_location_use_case
)

locations_router = APIRouter()

@locations_router.get("/", status_code=status.HTTP_200_OK, response_model=List[LocationResponse])
async def get_all_locations(use_case = Depends(get_all_locations_use_case)) -> List[LocationResponse]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/{location_id}", status_code=status.HTTP_200_OK, response_model=LocationResponse)
async def get_location_by_id(
    location_id: int,
    use_case = Depends(get_location_by_id_use_case)) -> LocationResponse:
    try:
        location = await use_case.execute(location_id=location_id)
        return location
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@locations_router.post(
    "/add_location",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationResponse,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def create_location(
    data: Location,
    use_case = Depends(create_location_use_case)) -> LocationResponse:
    try:
        location = await use_case.execute(data=data)
        return location
    except LocationNameIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@locations_router.delete(
    "/delete/{location_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def delete_location(
    location_id: int,
    use_case = Depends(delete_location_use_case)):
    try:
        await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
