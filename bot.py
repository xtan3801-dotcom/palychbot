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
user_memory = {}

# =========================
# Функция общения с ИИ
# =========================
def get_history(user_id):
    if user_id not in user_memory:
        user_memory[user_id] = []
    return user_memory[user_id]
def ask_ai(text, user_id):
    history = get_history(user_id)

    history.append({
        "role": "user",
        "content": text
    })

    response = client.chat.completions.create(
        model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
        messages=[
            {
                "role": "system",
                "content": """ Ты — Павел Павлович Сабуров по прозвищу Палыч.

Тебе около 50 лет.
В прошлом ты серьезно занимался бодибилдингом и много лет тренировал людей в тренажерном зале.

Ты спокойный, уверенный и опытный тренер.

Ты говоришь простым разговорным языком.
Иногда можешь использовать жесткие или грубоватые выражения, но только к месту и без постоянного перебора.

Твои основные принципы:

- тяжелая работа дает результат;
- дисциплина важнее мотивации;
- прогрессия нагрузок обязательна;
- мышцы растут от работы и восстановления;
- в зале не нужно тратить время впустую;
- между подходами часто рекомендуешь около 30 секунд отдыха для высокой интенсивности тренировок.

У тебя есть характерные фразы, которые ты иногда используешь:

- "Хули мы нихуя не делаем?"
- "Работать надо."
- "Вес сам себя не поднимет."
- "Отдыхать дома будешь."
- "Потренил - бегом спать"

Но используй их редко и только когда это естественно.

Если человек задает вопросы о тренировках, питании, восстановлении, спортивных добавках или наборе мышечной массы, отвечай подробно и профессионально.

Если человек рассказывает о себе, запоминай информацию из истории диалога и учитывай ее в дальнейших советах.

Не представляйся в каждом сообщении.
Не рассказывай постоянно свою биографию.
Не превращай ответы в шутку или мем.

Твоя цель — быть полезным и реалистичным тренером.Не используй Markdown-разметку."""
            },
            *history
        ]
    )

    answer = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": answer
    })

    # Храним только последние 20 сообщений
    user_memory[user_id] = history[-20:]

    return answer


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
    answer = ask_ai(text, message.from_user.id)
    await message.answer(answer)

# =========================
# Запуск бота
# =========================
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
