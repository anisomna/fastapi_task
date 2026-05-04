# fastapi_django_refactor

# Запуск с Docker
Запустите контейнеры:
- docker-compose up -d --build
При необходимости примените миграции:
- docker exec -it fastapi_backend alembic upgrade head

Завершить работу:
- docker-compose down