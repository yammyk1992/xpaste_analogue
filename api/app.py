from fastapi import FastAPI

from starlette.responses import JSONResponse

from api.schemas.schemas import TextForPOST
from api.views.service import get_text, post_text

app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("/{uuid}", tags=["GET TEXT"])
async def get_text_with_uuid(uuid: str) -> JSONResponse:
    data = await get_text(uuid)
    return JSONResponse({
        "schemas": str(data),
    })


@app.post("/", name="Post Text", tags=["CREATE TEXT"])
async def add_text(text_to_db: TextForPOST) -> JSONResponse:
    text = await post_text(text_to_db)
    return JSONResponse({
        "uuid": str(text)
    })
