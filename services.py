import uuid

import bcrypt
from sqlalchemy import select

import main
from database import get_session, Text as TextDB, Text


async def post_text(get_text):
    async with get_session() as session:
        get_uuid = uuid.uuid4()  # generate uuid4
        salt = bcrypt.gensalt().decode('utf-8')  # salt generate
        data = main.encrypt_data(salt, get_text.text)
        text_db_instance = TextDB(id=get_uuid, text=data,
                                  salt=salt)

        session.add(text_db_instance)
        await session.commit()
        await session.refresh(text_db_instance)
        return text_db_instance


async def get_text(text_id):
    async with get_session() as session:
        query = await session.execute(select(Text).where(Text.id == f"{text_id}"))
        text_db = query.scalars().all()
        if text_db:
            for i in text_db:
                return main.decrypt_data(i.salt, i.text)
        return None


async def get_text_for_delete():
    async with get_session() as session:
        query = await session.execute(select(TextDB.text_id))
        text_db = query.scalars().all()
        if len(text_db) > 0:
            return text_db[-1]
        else:
            return 0
