from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import AsyncGenerator

from config import POSTGRES_USER, POSTGRES_PASS, DB_PORT, DB_HOST, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(url=DATABASE_URL, echo=True)
Base = declarative_base()
async_session_maker = sessionmaker(engine=engine, class_=AsyncSession, expire_on_commit=False)


# Dependency
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
