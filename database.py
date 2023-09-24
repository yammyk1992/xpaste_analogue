from datetime import datetime
from contextlib import asynccontextmanager

from sqlalchemy import DateTime, String, Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import POSTGRES_USER, POSTGRES_PASS, DB_PORT, DB_HOST, DB_NAME

engine = create_async_engine(f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                             echo=True, future=True)


def async_session_generator():
    return async_sessionmaker(engine)


Base = declarative_base()


class Text(Base):

    __tablename__ = "text_create"

    text_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    text = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    salt = Column(String, nullable=True, default="")


# Теперь мы можем создать экземпляр AsyncSession и использовать его в нашем коде.
# Одним из лучших вариантов является создание контекстного менеджера, который закроет сеанс для нас,
# когда наш код перестанет его использовать. Важно отметить, что менеджер контекста не будет работать в
# асинхронной среде. Вместо этого мы должны использовать asynccontextmanager
@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
