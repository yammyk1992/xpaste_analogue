FROM python:3.10
EXPOSE 80
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false &&  \
    poetry install --no-dev --no-root --no-cache --no-interaction

COPY api ./api
COPY db ./db
COPY migrations ./migrations
COPY alembic.ini ./
COPY tasks ./tasks

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "80"]

