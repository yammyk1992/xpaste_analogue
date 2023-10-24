from datetime import datetime, timedelta

from sqlalchemy import select

from db.database import get_session
from db.models import Text


async def clean_data(token):
    time_now = datetime.utcnow()
    async with get_session() as session:
        query = await session.execute(
            select(Text).where(Text.text_uuid == f"{token}", Text.death_token))
        text_db = query.scalars().all()
        if not text_db:
            return True
        for i in text_db:
            if (time_now - i.created_at) >= timedelta(hours=2):
                await session.delete(i)
                await session.commit()
                return False
            return True

# def delete_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         session.delete(hero)
#         session.commit()
#         return {"ok": True}
# difference_time = timedelta(hours=24)
# d1 = datetime.fromisoformat("2023-10-21 11:46:26.773664")
# d = datetime.utcnow()
# d3 = d - d1
# print(difference_time)
# print(d3)
# print("yes" if d3 == difference_time else "no")
# time_now = datetime.utcnow()
# print(time_now + difference_time)
