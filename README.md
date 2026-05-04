# fastapi_django_refactor

# Запуск с Docker
Запустите контейнеры:
- docker-compose up -d --build
Примените миграции:
- docker exec -it fastapi_backend alembic upgrade head