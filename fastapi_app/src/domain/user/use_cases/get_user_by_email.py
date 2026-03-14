from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse as UserSchema
from fastapi import HTTPException, status


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_user_by_email(session, email)

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )

            user_dict = {
                "id": user.id,
                "login": user.login,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }

            return UserSchema.model_validate(obj=user_dict)
