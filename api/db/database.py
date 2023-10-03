from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from api.db.settings import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_pass}@{settings.db_host}:"
    f"{settings.db_port}/{settings.db_name}",
    echo=True,
    future=True,
)


def async_session_generator():
    return async_sessionmaker(engine)


Base = declarative_base()


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
