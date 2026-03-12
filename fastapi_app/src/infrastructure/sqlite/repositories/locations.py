from datetime import datetime
from typing import Type, List
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.locations import Location


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_all_locations(self, session: Session) -> List[Location]:
        query = session.query(self._model)
        return query.all()

    def get_location_by_id(self, session: Session, location_id: int) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == location_id)
        )
        return query.scalar()

    def get_published_locations(self, session: Session) -> List[Location]:
        query =(
            session.query(self._model)
            .where(self._model.is_published == True)
        )
        return query.all()

    def create_location(self, session: Session, 
        name: str, is_published: bool = True) -> Location:
        location = self._model(
            name=name,
            is_published=is_published,
            created_at=datetime.now()
        )
        session.add(location)
        session.flush()
        return location

    def delete_location(self, session: Session, location_id: int) -> bool:
        location = self.get_location_by_id(session, location_id)

        if location:
            session.delete(location)
            return True
        return False
