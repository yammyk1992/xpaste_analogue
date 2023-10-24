from fastapi import FastAPI

from api.schemas.xpaste import TextForPOST
from api.views.text import get_text, post_text

app = FastAPI(title="Xpaste application")


@app.get("/data/{token}", tags=["Get data"])
async def get_data(token: str) -> str:
    data = await get_text(token)
    return data


@app.post("/create/", tags=["Add data"])
async def post_data(text_to_db: TextForPOST) -> list:
    text = await post_text(text_to_db)
    return text

