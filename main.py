from cryptography.fernet import Fernet

from config import settings


# Шифруем
def encrypt_data(s, data):
    cipher_key = settings.secret_key + s
    cipher = Fernet(cipher_key)
    encrypted_text = cipher.encrypt(data.encode('utf-8'))
    return encrypted_text.decode('utf-8')


# Дешифруем
def decrypt_data(salt, encrypted_data):
    cipher_key = settings.secret_key + salt
    cipher = Fernet(cipher_key)
    text = cipher.decrypt(encrypted_data)
    return text

