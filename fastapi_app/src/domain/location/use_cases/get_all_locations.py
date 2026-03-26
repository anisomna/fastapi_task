from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponse as LocationSchema
from typing import List


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[LocationSchema]:
        with self._database.session() as session:
            locations = self._repo.get_all_locations(session)

            result = []
            for location in locations:
                result.append(LocationSchema.model_validate(obj=location))

            return result
