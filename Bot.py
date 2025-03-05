import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
import asyncio

# Настройки
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL, который выдаст Render
PORT = int(os.getenv("PORT", 5000))

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
async def telegram_webhook():
    """Обрабатываем запросы от Telegram"""
    update = Update(**request.json)
    await dp.feed_update(bot, update)
    return "OK", 200

async def set_webhook():
    """Устанавливаем Webhook"""
    await bot.set_webhook(WEBHOOK_URL + "/webhook")

# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())
    app.run(host="0.0.0.0", port=PORT)
