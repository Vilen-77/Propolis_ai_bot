from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Telegram-бот, подключённый через вебхук 🚀")

# Регистрируем все команды
def add_handlers(application: Application):
    application.add_handler(CommandHandler("start", start_command))
