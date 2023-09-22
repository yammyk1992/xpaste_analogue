import random
import string

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# функция получения соли
def get_salt():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))


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
