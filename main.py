from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import bcrypt

# получение ключа с солью
salt = bcrypt.gensalt()

text = b"ldkvjlskdmvlksmdlkvmslkdv"  # Replace with your own password

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA512(),
    length=64,  # 64 bytes = 512 bits
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = kdf.derive(text)

print(key, "ключи c солью")

# шифрование данных
cipher = Cipher(algorithms.AES(key), modes.XTS(key[:16]), backend=default_backend())

encryptor = cipher.encryptor()
padder = padding.PKCS7(128).padder()

padded_data = padder.update(text) + padder.finalize()
encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

print(encrypted_data, "зашифрованные данные")


# расшифрование данных
decryptor = cipher.decryptor()
unpadder = padding.PKCS7(128).unpadder()

decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

print(unpadded_data.decode("utf-8"), "расшифрованные данные")
