import uuid
import bcrypt

from sqlalchemy import select

from api.db.database import get_session
from api.db.models import Text, Text as TextDB
from api.schemas.schemas import TextForPOST
from api.views.utils import encrypt_data, decrypt_data


async def post_text(input_text: TextForPOST) -> str:
    async with get_session() as session:
        get_uuid = uuid.uuid4()
        salt = bcrypt.gensalt().decode('utf-8')
        data = encrypt_data(salt, input_text.text)
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
                return decrypt_data(i.salt, i.text)
        return None
