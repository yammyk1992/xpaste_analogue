from fastapi import FastAPI
from starlette.responses import JSONResponse

import models
from models import TextForPOST
from services import post_text, get_text
from database import Text as TextDB

app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("/", tags=["GET TEXT"])
async def get_last_text():
    data = get_text()
    return JSONResponse([
                            {
                                "text_id": t.text_id,
                                "text": t.text,
                                "created_at": str(t.created_at)
                            }
                            async for t in data
                        ][-1])


@app.post("/", name="Post Text", tags=["CREATE TEXT"])
async def add_text(item: TextForPOST):
    get_text = await post_text(TextDB(text=item.text, salt=models.get_salt()))
    return JSONResponse({
        "id": get_text.text_id,
        "text": get_text.text,
        "created_at": str(get_text.created_at)
    })


# @app.delete("/")
# async def delete_by_id() -> JSONResponse:
#     data = get_text()
#     return JSONResponse([
#                             {
#                                 "Status": "200",
#                                 "text_id": delete_text(int(t.text_id))
#                             }
#                             async for t in data
#                         ])
