from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.schemas.xpaste import TextForPOST
from api.views.text import get_text, post_text

app = FastAPI(title="Xpaste application")


@app.get("/data/{token}", tags=["Get data"])
async def get_data(token: str) -> JSONResponse:
    data = await get_text(token)
    return JSONResponse(
        {
            "data": str(data),
        }
    )


@app.post("/create/", tags=["Add data"])
async def post_data(text_to_db: TextForPOST) -> JSONResponse:
    text = await post_text(text_to_db)
    return JSONResponse(
        {
            "token": str(text),
        }
    )


