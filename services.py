import random
import string
from typing import AsyncIterator, Collection

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from sqlalchemy import select

from database import get_session, Text as TextDB
from models import TextForGET


async def post_text(get_text):
    async with get_session() as session:
        text_db_instance = TextDB(text=get_text.text, salt=get_text.salt)
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


# async def delete_text(data_id) -> JSONResponse:
#     async with get_session() as session:
#         query = await session.query(TextForGET).where(text_id=data_id)
#         await session.delete(query)
#         await session.commit()
#         return JSONResponse({
#             "status": '200'}
#         )


# функция получения рандомного пароля
def get_password():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(2))


# функция получения хэша с солью
def hash_with_salt(salt, data):
    hash_and_salt = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,  # 64 bytes = 512 bits
        salt=salt.encode("utf-8"),
        iterations=100000,
        backend=default_backend()
    )

    key = hash_and_salt.derive(get_password().encode("utf-8"))

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(data.encode("utf-8")) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data
