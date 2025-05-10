# Импортируем необходимые классы
from telegram import Update  # Объект Update содержит сообщение от пользователя
from telegram.ext import ContextTypes, CommandHandler, Application  # Обработчик и тип контекста

# Функция, которая будет вызвана, когда пользователь отправит команду /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ответим пользователю простым сообщением
    await update.message.reply_text("Привет! Я Telegram-бот, подключённый через вебхук 🚀")


# Функция для добавления обработчиков в приложение бота
def add_handlers(application: Application):
    # Создаём обработчик команды /start и связываем его с функцией start_command
    start_handler = CommandHandler("start", start_command)

    # Добавляем обработчик в приложение
    application.add_handler(start_handler)
