from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_session

app = FastAPI(title="text_project")


class Text(BaseModel):
    id: Optional[int] = None
    text: str
    created_at: Optional[datetime] = None
    salt: Optional[str] = None


@app.get("/text", response_model=list[Text])
async def get_text(session: AsyncSession = Depends(get_session)):
    import services
    texts = await services.get_text(session)
    return [Text(text=c.text, created_at=c.created_at) for c in texts]

#
# @app.post("/", response_model=Text, response_model_exclude={"salt", "id"})
# def create_txt(text: Text):
#     text.salt = services.get_salt()
#     text.created_at = datetime.utcnow()
#     return text

# @app.get("/")
# def read_text():
#     with Session(engine) as session:
#         heroes = session.select(select(Text)).all()
#         return heroes
# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         session.delete(hero)
#         session.commit()
#         return {"ok": True}
