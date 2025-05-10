from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from utils.ai_assistant import ask_openai

# ID владельца (админа)
ADMIN_CHAT_ID = 839647871

# Простая память: user_id → последнее сообщение (можно расширить)
pending_replies = {}

# Обработчик обычных текстов
async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    prompt = update.message.text

    # Получаем ответ от AI + флаг not_confident
    result = await ask_openai(prompt)
    reply_text = result["text"]
    not_confident = result["not_confident"]

    # Если не уверен — отправляем владельцу и клиенту временный ответ
    if not_confident:
        await update.message.reply_text("Момент, зараз дізнаюсь у власника...")

        notify = (
            f"❓ Запит від @{user.username or '—'} (ID: {user.id}):\n"
            f"{prompt}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=notify)

        # Сохраняем user_id
        pending_replies[user.id] = update.message.chat_id

    else:
        await update.message.reply_text(reply_text)

# Регистрируем хендлер
def add_handlers(application: Application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
