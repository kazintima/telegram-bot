import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8187256278:AAGHaVx0TQXitoU2dlgmU0m-fnDENFisanI"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список случайных советов
advice_list = [
    "Всегда проверяйте код на ошибки перед запуском!",
    "Учите Python каждый день – так будет проще!",
    "Используйте Google и Stack Overflow, если что-то не понятно.",
    "Автоматизируйте рутинные задачи – это сэкономит вам время!"
]

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Приветственное сообщение"""
    await message.answer("Привет! Я ваш Telegram-ассистент. Спросите меня что-нибудь!")

@dp.message(Command("advice"))
async def send_advice(message: types.Message):
    """Отправляет случайный совет"""
    advice = random.choice(advice_list)
    await message.answer(f"Совет дня: {advice}")

@dp.message()
async def assistant(message: types.Message):
    """Обрабатывает вопросы пользователя"""
    user_text = message.text.lower()

    if "как дела" in user_text:
        await message.answer("У меня всё отлично! А у вас?")
    elif "что ты умеешь" in user_text:
        await message.answer("Я могу отвечать на вопросы, давать советы и помогать с разными задачами!")
    else:
        await message.answer("Я пока не знаю ответа на этот вопрос, но учусь! 😊")

async def main():
    """Запуск бота"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import openai

OPENAI_API_KEY = "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"

async def assistant(message: types.Message):
    """Использует OpenAI для ответов"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.text}],
        api_key=OPENAI_API_KEY
    )
    await message.answer(response["choices"][0]["message"]["content"])

