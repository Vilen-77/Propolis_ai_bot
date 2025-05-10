import os
import openai
from openai import AsyncOpenAI

# Получаем ключ из переменной окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Создаём асинхронного клиента OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Запрос к GPT через ChatCompletion (новый формат)
async def ask_openai(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный Telegram-ассистент."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Произошла ошибка при обращении к AI: {e}"
