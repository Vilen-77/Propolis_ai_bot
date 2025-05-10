from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я AI-помічник типографії. Знаю майже все про компанію та відповідаю на більшість питань. Можу звернутись до власника або з'єднати Вас напряму. Чим можу допомогти зараз?")

# Регистрируем все команды
def add_handlers(application: Application):
    application.add_handler(CommandHandler("start", start_command))
