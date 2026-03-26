from datetime import datetime
from typing import Type, List
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.locations import Location
from schemas.location import Location as LocationSchema
from core.exceptions.database_exceptions import (
    LocationNotFoundException,
    LocationNameAlreadyExistsException
)


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_all_locations(self, session: Session) -> List[Location]:
        query = session.query(self._model)
        locations = query.all()

        if not locations:
            raise LocationNotFoundException()

        return locations

    def get_location_by_id(self, session: Session, location_id: int) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == location_id)
        )
        location = query.scalar()

        if not location:
            raise LocationNotFoundException()

        return location

    def get_published_locations(self, session: Session) -> List[Location]:
        query =(
            session.query(self._model)
            .where(self._model.is_published == True)
        )
        location = query.all()

        if not location:
            raise LocationNotFoundException()

        return location

    def create_location(self, session: Session, data: LocationSchema) -> Location:
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

    def delete_location(self, session: Session, location_id: int) -> None:
        location = self.get_location_by_id(session, location_id)

        if location:
            session.delete(location)
        else:
            raise LocationNotFoundException()
