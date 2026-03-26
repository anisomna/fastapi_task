from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse as UserSchema


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[UserSchema]:
        with self._database.session() as session:
            users = self._repo.get_all_users(session)

            result = []
            for user in users:
                result.append(UserSchema.model_validate(obj=user))

            return result
