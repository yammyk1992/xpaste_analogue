from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import bcrypt

# получение ключа с солью
import services


def hash_with_salt(data):
    salt = bcrypt.gensalt()

    hash_and_salt = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,  # 64 bytes = 512 bits
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = hash_and_salt.derive(data.encode("utf-8"))

    return key


def get_encryptor_data(key, data):

    key_byte = key

    cipher = Cipher(algorithms.AES(key_byte), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(data.encode("utf-8")) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_data


# # расшифрование данных
# decryptor = cipher.decryptor()
# unpadder = padding.PKCS7(128).unpadder()
#
# decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
# unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
#
# print(unpadded_data.decode("utf-8"), "расшифрованные данные")
