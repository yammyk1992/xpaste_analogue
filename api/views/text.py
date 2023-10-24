import uuid
from datetime import datetime, timedelta
from typing import List

import bcrypt
from fastapi import HTTPException
from sqlalchemy import select

from db.database import get_session
from db.models import Text
from db.models import Text as TextDB
from api.schemas.xpaste import TextForPOST
from api.service.data_encription import decrypt_data, encrypt_data

from tasks.tasks import clean_data_after_24_hours, clean_data_after_3_days


async def post_text(input_text: TextForPOST) -> List:
    async with get_session() as session:
        get_uuid = uuid.uuid4()
        salt = bcrypt.gensalt().decode("utf-8")
        data = encrypt_data(salt, input_text.text)
        text_db_instance = TextDB(text_uuid=get_uuid, text=data, salt=salt, death_token=input_text.death_token,
                                  created_at=datetime.utcnow())

        session.add(text_db_instance)
        await session.commit()
        await session.refresh(text_db_instance)

        if text_db_instance.death_token:
            # Celery task
            clean_data_after_24_hours.apply_async(eta=datetime.utcnow() + timedelta(seconds=10))
            return [text_db_instance.text_uuid, "expired after 24 hours"]
        # Celery task
        clean_data_after_3_days.apply_async(eta=datetime.utcnow() + timedelta(seconds=10))
        return [text_db_instance.text_uuid, "expired after 3 days"]


async def get_text(text_id: str) -> str | None:
    async with get_session() as session:
        query = await session.execute(
            select(Text).where(Text.text_uuid == f"{text_id}")
        )
        text_db = query.scalars().all()
        if text_db:
            for i in text_db:
                return decrypt_data(i.salt, i.text)

        raise HTTPException(status_code=404, detail="Text not found, maybe your token is expired")
