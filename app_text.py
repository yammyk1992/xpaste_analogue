from fastapi import FastAPI

from starlette.responses import JSONResponse

from models import TextForPOST
from services import post_text, get_text

# 1. Post
# Генерация uuid4, генерация соли
# Создание ключа config.SECRET_KEY + salt
# aes512.encrypt(key=config.SECRET_KEY + salt, input_text)
# db.insert()
# return uuid4
#
# 2. GET
# db.select(id=uuid4)
# aes512.decrypt(key=config.SECRET_KEY + db_row.salt)
# return text

app = FastAPI(title="APP TEXT", description="APP with ADD Text")


@app.get("/{uuid}", tags=["GET TEXT"])
async def get_last_text(uuid):
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


# @app.delete("/", name="Delete Text", tags=["DELETE TEXT"])
# async def delete_text(item: int = Depends(services.get_text_for_delete)):
#     async with get_session() as session:
#         text = await session.get(TextDB, item)
#         if not text:
#             raise HTTPException(status_code=404, detail="DB Empty")
#         await session.delete(text)
#         await session.commit()
#         return {"ok": True}
