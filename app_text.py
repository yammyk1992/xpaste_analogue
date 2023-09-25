from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.responses import JSONResponse

import models
import services
from models import TextForPOST
from services import post_text, get_text
from database import Text as TextDB, get_session

app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("/", tags=["GET TEXT"])
async def get_last_text(request: Request):
    data = get_text()
    return JSONResponse([
                            {
                                "text_id": t.text_id,
                                "text": t.text,
                                "created_at": str(t.created_at)

                            }
                            async for t in data
                        ])


@app.post("/", name="Post Text", tags=["CREATE TEXT"])
async def add_text(item: TextForPOST, request: Request):
    get_text = await post_text(TextDB(text=item.text, salt=models.get_salt()))
    return JSONResponse({
        "id": get_text.text_id,
        "text": get_text.text,
        "created_at": str(get_text.created_at),
        "url": str(request.url)
    })


@app.delete("/", name="Delete Text", tags=["DELETE TEXT"])
async def delete_text(item: int = Depends(services.get_text_for_delete)):
    async with get_session() as session:
        text = await session.get(TextDB, item)
        if not text:
            raise HTTPException(status_code=404, detail="DB Empty")
        await session.delete(text)
        await session.commit()
        return {"ok": True}
