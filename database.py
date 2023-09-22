from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import AsyncGenerator

from config import POSTGRES_USER, POSTGRES_PASS, DB_PORT, DB_HOST, DB_NAME

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()

# create engine for interaction with database
engine = create_engine(DATABASE_URL)

# create session for the interaction with database
sessions_maker = sessionmaker(engine=engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessions_maker() as session:
        yield session
