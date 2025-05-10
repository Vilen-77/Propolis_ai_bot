from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application
from utils.ai_assistant import ask_openai

# Обработчик всех текстовых сообщений (не команд)
async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await ask_openai(user_text)
    await update.message.reply_text(reply)

# Регистрируем в приложение
def add_handlers(application: Application):
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response)
    )
