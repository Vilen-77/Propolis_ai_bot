import os
import openai

# Получаем API-ключ из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

# Простая функция: передаём текст — получаем ответ
async def ask_openai(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",  # можно позже сменить
            messages=[
                {"role": "system", "content": "Ты дружелюбный Telegram-ассистент."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Произошла ошибка при обращении к AI: {e}"
