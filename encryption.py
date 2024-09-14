import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class EncryptionManager:
    def __init__(self):
        self.key = self.load_key()

    def load_key(self):
        key_path = r"C:\Users\Administrator\Desktop\key.txt"
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                key = f.read()
            if len(key) in (16, 24, 32):  # Проверяем допустимые размеры ключа для AES
                return key
            else:
                raise Exception("Неверный размер ключа шифрования")
        else:
            raise Exception(f"Ключ шифрования не найден по пути: {key_path}")

    def encrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        serialized_data = str(data).encode('utf-8')
        ct_bytes = cipher.encrypt(pad(serialized_data, AES.block_size))
        return cipher.iv + ct_bytes

    def decrypt_data(self, encrypted_data):
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        data = eval(pt.decode('utf-8'))
        return data
