import asyncio

from celery import Celery
from sqlalchemy import select

from db.database import get_session
from db.models import Text

app = Celery('tasks', broker='redis://redis:6379/0')


@app.task(name="Delete from db after 24 hours")
def clean_data_after_24_hours():
    async def clean_data():
        async with get_session() as session:
            query = await session.execute(select(Text).where(Text.death_token == True))
            text_db = query.scalars().all()
            for i in text_db:
                await session.delete(i)
                await session.commit()

    asyncio.run(clean_data())

    return "will delete after 24 hours"


@app.task(name="Delete from db after 3 days")
def clean_data_after_3_days():
    async def clean_data():
        async with get_session() as session:
            query = await session.execute(select(Text).where(Text.death_token == False))
            text_db = query.scalars().all()
            for i in text_db:
                await session.delete(i)
                await session.commit()

    asyncio.run(clean_data())

    return "will delete after 3 days"
