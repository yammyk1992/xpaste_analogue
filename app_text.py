from fastapi import FastAPI
from starlette.responses import JSONResponse

import models
from models import Text
from services import post_text
from database import Text as TextDB


app = FastAPI(title="APP TEXT")


# @app.get("/", response_model=None)
# async def get_text():
#     async_session = async_session_generator()
#     async with async_session() as session:
#         query = await session.execute(select(Text))
#         text_db = query.scalars().all()
#         await session.close()
#         return JSONResponse([{"txt": t.text,
#                               "created_at": t.created_at}
#                              async for t in text_db])

@app.post("/", response_model=None)
async def add_text(item: Text):
    tutorial = await post_text(TextDB(text=item.text, salt=models.get_salt()))
    return JSONResponse({
        "text": tutorial.text
    })
