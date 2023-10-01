from fastapi import FastAPI

from starlette.responses import JSONResponse

from models import TextForPOST
from services import post_text, get_text


app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("/{uuid}", tags=["GET TEXT"])
async def get_text_with_uuid(uuid):
    data = await get_text(uuid)
    return JSONResponse({
        "text": str(data.decode('utf-8'))
    })


@app.post("/", name="Post Text", tags=["CREATE TEXT"])
async def add_text(text_to_db: TextForPOST):
    text = await post_text(text_to_db)
    return JSONResponse({
        "uuid": str(text.id)
    })
