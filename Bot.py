import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("Переменная окружения TOKEN не установлена!")

import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
import asyncio

# Настройки
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 5000))

if not TOKEN:
    raise ValueError("Переменная окружения TOKEN не установлена!")

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

@dp.message()
async def echo(message: types.Message):
    """Обработчик сообщений"""
    await message.answer(f"Вы сказали: {message.text}")

@app.route("/", methods=["GET"])
def home():
    return "Бот работает!"

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    """Обрабатываем запросы от Telegram"""
    update = Update(**request.json)
    asyncio.run(dp.feed_update(bot, update))  # Исправляем ошибку Flask
    return "OK", 200

@app.before_first_request
def activate_webhook():
    """Настраиваем Webhook при первом запросе"""
    asyncio.run(set_webhook())

async def set_webhook():
    """Устанавливаем Webhook"""
    await bot.set_webhook(WEBHOOK_URL + "/webhook")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

