from fastapi import FastAPI

from starlette.responses import JSONResponse

from api.router.router import data_router, create_data
from api.schemas import TextForPOST
from api.views.utils import get_text, post_text

app = FastAPI(title="Xpaste application")


@data_router.get("/{token}")
async def get_data(token: str) -> JSONResponse:
    data = await get_text(token)
    return JSONResponse({
        "data": str(data),
    })


@create_data.post("/")
async def post_data(text_to_db: TextForPOST) -> JSONResponse:
    text = await post_text(text_to_db)
    return JSONResponse({
        "token": str(text)
    })


app.include_router(data_router)
app.include_router(create_data)
