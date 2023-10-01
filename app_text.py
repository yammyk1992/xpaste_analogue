from fastapi import FastAPI
from models import TextForPOST
from services import get_text, post_text
from starlette.responses import JSONResponse

app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("/{uuid}", tags=["GET TEXT"])
async def get_text_with_uuid(uuid: str) -> JSONResponse:
    data = await get_text(uuid)
    return JSONResponse({
        "text": str(data),
    })


@app.post("/", name="Post Text", tags=["CREATE TEXT"])
async def add_text(text_to_db: TextForPOST) -> JSONResponse:
    text = await post_text(text_to_db)
    return JSONResponse({
        "uuid": str(text)
    })
