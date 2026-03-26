from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponse as LocationSchema, Location
from core.exceptions.database_exceptions import LocationNameAlreadyExistsException
from core.exceptions.domain_exceptions import LocationNameIsNotUniqueException
import logging

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: Location) -> LocationSchema:
        with self._database.session() as session:
            try:
                location = self._repo.create_location(session=session, data=data)
            except LocationNameAlreadyExistsException:
                error = LocationNameIsNotUniqueException(name=data.name)
                logger.error(error.get_detail())
                raise error

            return LocationSchema.model_validate(obj=location)
