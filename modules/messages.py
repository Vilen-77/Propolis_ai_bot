from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from utils.ai_assistant import ask_openai
from utils.memory_google import load_memory_from_drive, save_memory_to_drive
import os

ADMIN_CHAT_ID = 839647871
pending_replies = {}

def load_tag_knowledge(tag: str) -> str:
    filename = f"utils/knowledge_{tag.lower()}.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return ""

async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    prompt = update.message.text
    user_id = user.id

    try:
        history = load_memory_from_drive(user_id)
    except Exception:
        history = ""

    # Первый вызов
    result = await ask_openai(prompt, history)
    reply_text = result["text"]
    not_confident = result["not_confident"]
    extra_tag = result.get("extra_tag")

    # Если есть тег — повторно вызываем с доп. знанием
    if extra_tag:
        extra_knowledge = load_tag_knowledge(extra_tag)
        if extra_knowledge:
            result = await ask_openai(prompt, history, extra_knowledge)
            reply_text = result["text"]
            not_confident = result["not_confident"]

    # Сохраняем в память
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

def add_handlers(application: Application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
