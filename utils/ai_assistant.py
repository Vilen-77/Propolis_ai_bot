import os
from openai import AsyncOpenAI

# Инициализация клиента OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Универсальная функция чтения текстовых файлов
def load_text_file(filename: str, fallback: str = "") -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception:
        return fallback

# Загружаем файл с правилами общения (стиль, язык и т.д.)
SYSTEM_PROMPT = load_text_file("utils/assistant_prompt.txt", "Ти — асистент у Telegram.")

# Загружаем файл с предметной информацией (товары, услуги, сайт)
KNOWLEDGE_CONTEXT = load_text_file("utils/assistant_knowledge.txt", "")

# Основная функция: отправляем вопрос в OpenAI и получаем ответ
async def ask_openai(prompt: str) -> str:
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        # Добавляем предметную базу знаний (если есть)
        if KNOWLEDGE_CONTEXT:
            messages.append({"role": "system", "content": f"Корисна інформація:\n{KNOWLEDGE_CONTEXT}"})

        # Добавляем сообщение от пользователя
        messages.append({"role": "user", "content": prompt})

        # Отправляем запрос к OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Помилка AI: {e}"
