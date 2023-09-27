from typing import List

from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.responses import JSONResponse

import models
import services
from models import TextForPOST
from services import post_text, get_text
from database import Text as TextDB, get_session

app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("get_text/", tags=["GET TEXT"])
async def get_last_text():
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
async def add_text(text_to_db: TextForPOST):
    get_text = await post_text(text_to_db)
    return JSONResponse({
        "uuid": str(get_text.id),
        "key_with_salt": get_text.key_with_salt
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
