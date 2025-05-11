# Тестовое задание

## Сборка проекта в контейнере

1. sudo docker compose up -d

## Локальный запуск
1. sudo docker compose -f docker-compose.local.yaml up -d
2. в app/config/settings изменить значение env_file на env.local
3. Применить миграции через
   ```alembic upgrade head```
4. Запуск проекта через ``main.py``
5. 