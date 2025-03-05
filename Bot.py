import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения из .env
logger.info("Загрузка переменных из .env...")
env_path = os.path.join(os.getcwd(), ".env")
logger.info(f"Путь к .env: {env_path}")
load_dotenv(env_path)

# Получаем переменные окружения
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 5000))

# Отладочный вывод
logger.info(f"TOKEN: {TOKEN}")
logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")
logger.info(f"PORT: {PORT}")

# Проверяем наличие обязательных переменных
if not TOKEN:
    logger.error("Переменная окружения TOKEN не установлена!")
    raise ValueError("Переменная окружения TOKEN не установлена!")
if not WEBHOOK_URL:
    logger.error("Переменная окружения WEBHOOK_URL не установлена!")
    raise ValueError("Переменная окружения WEBHOOK_URL не установлена!")

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
    asyncio.run(dp.feed_update(bot, update))
    return "OK", 200

async def set_webhook():
    """Устанавливаем Webhook"""
    await bot.set_webhook(WEBHOOK_URL + "/webhook")
    logger.info(f"Webhook установлен на {WEBHOOK_URL}/webhook")

def run_bot():
    """Запускаем бота и устанавливаем вебхук при старте"""
    asyncio.run(set_webhook())

if __name__ == "__main__":
    logger.info(f"Запуск бота на порту {PORT}")
    run_bot()  # Устанавливаем вебхук перед запуском Flask
    app.run(host="0.0.0.0", port=PORT)
