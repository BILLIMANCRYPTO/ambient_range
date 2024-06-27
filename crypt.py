import pyAesCrypt

# Пароль для шифрования (замените на свой пароль)
password = ""

# Зашифруйте файл wallets.txt
pyAesCrypt.encryptFile("wallets.txt", "wallets.txt.aes", password)
