from cryptography.fernet import Fernet

from api.db.settings import settings


def encrypt_data(salt: str, data: str) -> str:
    cipher_key = settings.secret_key + salt
    cipher = Fernet(cipher_key)
    encrypted_text = cipher.encrypt(data.encode('utf-8'))
    return encrypted_text.decode('utf-8')


# Дешифруем
def decrypt_data(salt: str, encrypted_data: bytes) -> str:
    cipher_key = settings.secret_key + salt
    cipher = Fernet(cipher_key)
    text = cipher.decrypt(encrypted_data).decode('utf-8')
    return text
