import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_text_file(filename: str, fallback: str = "") -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception:
        return fallback

# Загружаем инструкции
SYSTEM_PROMPT = load_text_file("utils/assistant_prompt.txt", "Ти — AI-помічник.")
KNOWLEDGE_CONTEXT = load_text_file("utils/assistant_knowledge.txt", "")

# Основная функция: запрос к GPT + определение уверенности
async def ask_openai(prompt: str, history: str = "") -> dict:
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if KNOWLEDGE_CONTEXT:
            messages.append({"role": "system", "content": f"Корисна інформація:\n{KNOWLEDGE_CONTEXT}"})

        if history:
            messages.append({"role": "system", "content": f"Контекст попередньої розмови:\n{history}"})

        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )

        reply_raw = response.choices[0].message.content.strip()
        reply = reply_raw.lower()

        not_confident = "[ask_owner]" in reply
        reply_clean = reply_raw.replace("[ASK_OWNER]", "").strip()

             return {
            "text": reply_clean,
            "not_confident": not_confident,
            "raw": reply_raw  # сырой ответ GPT
        }

    except Exception as e:
        return {
            "text": f"⚠️ Помилка AI: {e}",
            "not_confident": True
        }
