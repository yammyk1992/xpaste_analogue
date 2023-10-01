import uuid
import bcrypt
from database import Text as TextDB, Text, get_session
import main
from sqlalchemy import select

from models import TextForPOST


async def post_text(input_text: TextForPOST) -> str:
    async with get_session() as session:
        get_uuid = uuid.uuid4()
        salt = bcrypt.gensalt().decode('utf-8')
        data = main.encrypt_data(salt, input_text.text)
        text_db_instance = TextDB(text_uuid=get_uuid, text=data,
                                  salt=salt)

        session.add(text_db_instance)
        await session.commit()
        await session.refresh(text_db_instance)
        return text_db_instance.text_uuid


async def get_text(text_id: str) -> str | None:
    async with get_session() as session:
        query = await session.execute(select(Text).
                                      where(Text.text_uuid == f"{text_id}"))
        text_db = query.scalars().all()
        if text_db:
            for i in text_db:
                return main.decrypt_data(i.salt, i.text)
        return None


# async def get_text_for_delete():
#     async with get_session() as session:
#         query = await session.execute(select(TextDB.text_id))
#         text_db = query.scalars().all()
#         if len(text_db) > 0:
#             return text_db[-1]
#         else:
#             return 0
