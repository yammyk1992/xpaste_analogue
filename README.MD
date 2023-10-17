Создания и запуск приложения в контейнере

Создание networking
docker network create xpaste

Cоздание image
docker build . -t new-app:latest

Запуск бд!
docker run -d \
    --name db\
    --hostname xpaste \
    --network xpaste --network-alias postgres \
    -v postgres-data:/var/lib/mysql \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=postgres \
    -e POSTGRES_USER=postgres \
-p 5440:5432 \
postgres

Запуск приложения!
docker run \
    -e SECRET_KEY=_wCCQ6Zg4FGrn34Dm2_RPtlUf4wN5H5jB_1Uww--lcg= \
    -e DATABASE_URL=postgresql+asyncpg://postgres:postgres@xpaste:5432/postgres \
    --network xpaste \
    -dp 8012:80 new-app


http://127.0.0.1:8012/docs