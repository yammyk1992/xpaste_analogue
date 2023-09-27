import random
import string
import uuid
from typing import AsyncIterator

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from sqlalchemy import select

import main
from database import get_session, Text as TextDB
from models import TextForGET


async def post_text(get_text):
    async with get_session() as session:
        get_uuid = uuid.uuid4()
        data = get_text.text
        key = main.hash_with_salt(str(get_uuid))
        text_to_encryptor = main.get_encryptor_data(key, data)
        text_db_instance = TextDB(id=get_uuid, text=str(text_to_encryptor),
                                  key_with_salt=str(key))

        session.add(text_db_instance)
        await session.commit()
        await session.refresh(text_db_instance)
        return text_db_instance


async def get_text() -> AsyncIterator[TextForGET]:
    async with get_session() as session:
        query = await session.execute(select(TextDB))
        text_db = query.scalars().all()
        for t in text_db:
            yield TextForGET(text_id=t.text_id, text=t.text, created_at=t.created_at)


async def get_text_for_delete():
    async with get_session() as session:
        query = await session.execute(select(TextDB.text_id))
        text_db = query.scalars().all()
        if len(text_db) > 0:
            return text_db[-1]
        else:
            return 0


# функция получения рандомного пароля
def get_password():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(2))


# функция получения хэша с солью
def hash_with_salt(salt, data):
    hash_and_salt = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=64,  # 64 bytes = 512 bits
        salt=salt.encode("utf-8"),
        iterations=100000,
        backend=default_backend()
    )

    key = hash_and_salt.derive(data.encode("utf-8"))

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(data.encode("utf-8")) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data
