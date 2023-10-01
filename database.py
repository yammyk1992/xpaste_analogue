import uuid
from contextlib import asynccontextmanager
from config import settings

from sqlalchemy import Column, String, UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}",
    echo=True, future=True)


def async_session_generator():
    return async_sessionmaker(engine)


Base = declarative_base()


class Text(Base):
    __tablename__ = "text_create"

    text_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    text = Column(String(255), nullable=False)
    salt = Column(String, nullable=False)


# Одним из лучших вариантов является создание контекстного менеджера, который закроет сеанс для нас,
# когда наш код перестанет его использовать.
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
