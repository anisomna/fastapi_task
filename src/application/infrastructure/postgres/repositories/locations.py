from datetime import datetime
from typing import Type, List
from sqlalchemy import insert, select
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
        query = session.query(self._model)
        locations = query.all()

        if not locations:
            raise LocationNotFoundException()

        return locations

    async def get_location_by_id(self, session: AsyncSession, location_id: int) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == location_id)
        )
        location = query.scalar()

        if not location:
            raise LocationNotFoundException()

        return location

    async def get_published_locations(self, session: AsyncSession) -> List[Location]:
        query =(
            session.query(self._model)
            .where(self._model.is_published == True)
        )
        location = query.all()

        if not location:
            raise LocationNotFoundException()

        return location

    async def create_location(self, session: AsyncSession, data: LocationSchema) -> Location:
        existing_location = session.scalar(
            select(self._model).where(self._model.name == data.name)
        )

        if existing_location is not None:
            raise LocationNameAlreadyExistsException()
    
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        location = session.scalar(query)

        return location

    async def delete_location(self, session: AsyncSession, location_id: int) -> None:
        location = self.get_location_by_id(session, location_id)

        if location:
            session.delete(location)
        else:
            raise LocationNotFoundException()
