from typing import List
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import LocationRepository
from application.schemas.locations import LocationResponse as LocationSchema


class GetPublishedLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[LocationSchema]:
        with self._database.session() as session:
            locations = self._repo.get_published_locations(session)

            result = []
            for location in locations:
                result.append(LocationSchema.model_validate(obj=location))

            return result
