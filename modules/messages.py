from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from utils.ai_assistant import ask_openai
from utils.memory_google import load_memory_from_drive, save_memory_to_drive

# ID владельца (админа)
ADMIN_CHAT_ID = 839647871

# Простая память: user_id → последнее сообщение (можно расширить)
pending_replies = {}

# Обработчик обычных текстов
async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    prompt = update.message.text
    user_id = user.id

    # Загружаем память пользователя
    try:
        history = load_memory_from_drive(user_id)
    except Exception:
        history = ""

    # Первый вызов GPT (без доп. знаний)
    result = await ask_openai(prompt, history)
    reply_text = result["text"]
    not_confident = result["not_confident"]
    raw = result.get("raw", "")

    # Показываем отладочный ответ GPT
    await update.message.reply_text(f"[DEBUG] RAW: {raw}")

    # Если GPT вставил тег [BYRKI], повторно вызываем с дополнительной информацией
    if "[BYRKI]" in raw:
        try:
            with open("utils/knowledge_BYRKI.txt", "r", encoding="utf-8") as f:
                extra_knowledge = f.read().strip()
        except Exception:
            extra_knowledge = ""

        # Повторный вызов GPT с доп. знанием
        result = await ask_openai(prompt, history, extra_knowledge=extra_knowledge)
        reply_text = result["text"]
        not_confident = result["not_confident"]

    # Сохраняем в историю
    save_memory_to_drive(user_id, f"👤 {prompt}\n🤖 {reply_text}")

    if not_confident:
        await update.message.reply_text("Момент, зараз дізнаюсь у власника...")

        notify = (
            f"❓ Запит від @{user.username or '—'} (ID: {user.id}):\n"
            f"{prompt}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=notify)
        pending_replies[user.id] = update.message.chat_id
    else:
        await update.message.reply_text(reply_text)

# Регистрируем хендлер
def add_handlers(application: Application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
