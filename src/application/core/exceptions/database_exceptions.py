class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundException(BaseDatabaseException):
    _exception_text_template = "Не найдено пользователей"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class UserLoginAlreadyExistsException(BaseDatabaseException):
    _exception_text_template = "Пользователь с таким логином уже существует"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class UserEmailAlreadyExistsException(BaseDatabaseException):
    _exception_text_template = "Пользователь с такой почтой уже существует"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundException(BaseDatabaseException):
    _exception_text_template = "Не найдено категорий"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class CategorySlugAlreadyExistsException(BaseDatabaseException):
    _exception_text_template = "Категория с таким slug уже существует"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class LocationNotFoundException(BaseDatabaseException):
    _exception_text_template = "Не найдено локаций"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class LocationNameAlreadyExistsException(BaseDatabaseException):
    _exception_text_template = "Локация с таким именем уже существует"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class PostNotFoundException(BaseDatabaseException):
    _exception_text_template = "Не найдено публикаций"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class CommentNotFoundException(BaseDatabaseException):
    _exception_text_template = "Не найдено комментариев"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)
