# modules/ai_assistant.py

# Импорт для Telegram-бота
from telegram import Update
from telegram.ext import ContextTypes
import os

# Импорт библиотеки OpenAI
import openai

# Загружаем ключ API из переменной окружения
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Асинхронная функция — обработчик команды /ask
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    ADMIN_USERNAME = "Vilen77"

    # Только админ может использовать AI
    if username != ADMIN_USERNAME:
        await update.message.reply_text("⛔ У Вас нет доступа к этой команде.")
        return

    # Получаем текст запроса после команды /ask
    if context.args:
        user_prompt = " ".join(context.args)
    else:
        await update.message.reply_text("ℹ️ Напишите вопрос после команды /ask.")
        return

    try:
        # Отправляем запрос в OpenAI ChatGPT (GPT-4 или GPT-3.5)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Можно заменить на "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Ты умный помощник на русском языке."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # Извлекаем ответ
        ai_reply = response["choices"][0]["message"]["content"]

        # Отправляем ответ в чат
        await update.message.reply_text(ai_reply)

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка запроса: {e}")
