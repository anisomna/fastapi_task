from pydantic import SecretStr
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from infrastructure.sqlite.models.users import User as UserModel
from schemas.users import UserCreate

class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserCreate:
        with self._database.session() as session:
            existing = self._repo.get_user_by_login(session, data.login)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь с таким логином уже существует"
                )

            user = UserModel(
                login=data.login,
                email=data.email,
                first_name=data.first_name,
                last_name=data.last_name,
                password=data.password
            )

            created = self._repo.create_user(session, user)
            return UserCreate.model_validate(created, from_attributes=True)
