import pyAesCrypt
import os
import requests
import pandas as pd
from datetime import datetime
import time
from colorama import Fore, Style, init
import telebot

# Initialize Colorama
init(autoreset=True)

# Пароль для дешифрования файла с кошельками
password = ""  # Введите сюда ваш пароль

# Дешифрование файла с кошельками
bufferSize = 64 * 1024
pyAesCrypt.decryptFile("wallets.txt.aes", "wallets_decrypted.txt", password, bufferSize)

# Чтение адресов кошельков из файла
with open("wallets_decrypted.txt") as file:
    wallets = [line.strip() for line in file]

# Удаление временного файла после чтения
os.remove("wallets_decrypted.txt")

# Telegram bot token and chat ID
telegram_token = '' # Api key своего бота https://t.me/BotFather
chat_id = '' # свой chatid https://t.me/chatIDrobot

# Initialize Telegram bot
bot = telebot.TeleBot(telegram_token)

# API URL
base_url = "https://ambindexer.net/scroll-gcgo/user_positions"

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def check_positions():
    for wallet in wallets:
        params = {
            'user': wallet,
            'chainId': '0x82750',
            'ensResolution': 'true',
            'annotate': 'true',
            'omitEmpty': 'true',
            'omitKnockout': 'true',
            'addValue': 'true'
        }

        response = requests.get(base_url, params=params)
        response_data = response.json()

        for position in response_data.get('data', []):
            concLiq = position.get('concLiq', 0)
            if concLiq == 0:
                continue  # Skip processing if concLiq is 0

            aprEst = position.get('aprEst', 'N/A')
            timeFirstMint = position.get('timeFirstMint', 0)
            wallet_address = position.get('user', wallet)

            if aprEst == 0:
                print("🟥 Out Range 🟥")
                message = f"🟥 {wallet_address} - Ambient: [Position Opened {convert_timestamp(timeFirstMint)}]-🟥 Out Range 🟥"

                bot.send_message(chat_id, message)
            else:
                print("🟢 In Range 🟢")
                message = f"🟢 {wallet_address} - Ambient: [Position Opened {convert_timestamp(timeFirstMint)}]-🟢 In Range 🟢"

                # Commented out the line to avoid sending "In Range" messages
                # bot.send_message(chat_id, message)

while True:
    check_positions()
    time.sleep(10*60*60)  # Настрой через сколько секунд будет происходить повторная проверка пула 60*60 = 1 час , 20*60*60 = 20 часов и тд либо просто укажи число в секундах 600 = 10 минут