import os

# Генерируем 16-байтный ключ для AES-128
key = os.urandom(16)

# Сохраняем ключ в файл
key_path = 'C:\\Users\\Administrator\\Desktop\\key.txt'
with open(key_path, 'wb') as f:
    f.write(key)

print(f"Ключ успешно сохранен по пути: {key_path}")
