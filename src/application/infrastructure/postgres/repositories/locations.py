from datetime import datetime
from typing import Type, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.models.locations import Location
from application.schemas.locations import Location as LocationSchema
from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
    LocationNameAlreadyExistsException
)


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    async def get_all_locations(self, session: AsyncSession) -> List[Location]:
        query = select(self._model)
        result = await session.execute(query)
        locations = result.scalars().all()

        if not locations:
            raise LocationNotFoundException()

        return locations

    async def get_location_by_id(self, session: AsyncSession, location_id: int) -> Location:
        query = select(self._model).where(self._model.id == location_id)
        result = await session.execute(query)
        location = result.scalar_one_or_none()

        if not location:
            raise LocationNotFoundException()

        return location

    async def get_published_locations(self, session: AsyncSession) -> List[Location]:
        query = select(self._model).where(self._model.is_published == True)
        result = await session.execute(query)
        locations = result.scalars().all()

        if not locations:
            raise LocationNotFoundException()

        return locations

    async def create_location(self, session: AsyncSession, data: LocationSchema) -> Location:
        existing_query = select(self._model).where(self._model.name == data.name)
        existing_result = await session.execute(existing_query)
        existing_location = existing_result.scalar_one_or_none()

        if existing_location is not None:
            raise LocationNameAlreadyExistsException()
        
        location_data = data.model_dump(exclude_none=True)
        location = self._model(**location_data)
        session.add(location)
        await session.flush()
        await session.refresh(location)

        return location

    async def delete_location(self, session: AsyncSession, location_id: int) -> None:
        location = await self.get_location_by_id(session, location_id)

        if location:
            await session.delete(location)
            await session.flush()
        else:
            raise LocationNotFoundException()
