from typing import List
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse as UserSchema


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[UserSchema]:
        async with self._database.session() as session:
            users = await self._repo.get_all_users(session)

            result = []
            for user in users:
                result.append(UserSchema.model_validate(obj=user))

            return result
