from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F
import asyncio 
import os
from openai import OpenAI

# =========================
# НАСТРОЙКИ
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# OpenRouter
# =========================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# =========================
# Telegram
# =========================
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# =========================
# Функция общения с ИИ
# =========================
def ask_ai(text):
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[
            {
                "role": "system",
                "content": """Ты — бодибилдер и тренер Сабуров Павел(Палыч). Твои правила:
- отвечай все про накачку мышц;
- обращайся на "ты".
- не диктуй всю информацию о себе.
твои принципы: любишь составлять жесткие тренировки для наращивания мышечной массы с отдыхом 30 секунд между подходами."""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content

# =========================
# Команда /start
# =========================
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Напиши мне что-нибудь.")

# =========================
# Любое сообщение
# =========================
@dp.message(F.text)
async def chat(message: Message):
    text = message.text
    answer = ask_ai(text)
    await message.answer(answer)

# =========================
# Запуск бота
# =========================
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
