# modules/get_log_file.py

# Импорты для Telegram
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

# Импорт для проверки наличия файла
import pathlib

# Асинхронная функция для отправки лог-файла по команде /getlog
# Принимает: объект обновления (сообщение), и контекст (бот, чат и др.)
async def getlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем Telegram username пользователя
    username = update.effective_user.username

    # Здесь должно быть имя админа — мы импортируем его из bot.py или задаём прямо тут
    # Но лучше передавать как параметр (см. ниже)
    ADMIN_USERNAME = "Vilen77"

    # Имя файла лога, который мы хотим отправить
    log_path = "log_stea_verde.txt"

    # Проверка: если пользователь — не админ, запрещаем команду
    if username != ADMIN_USERNAME:
        await update.message.reply_text("⛔ У Вас нет доступа к этой команде.")
        return

    # Проверяем, существует ли файл
    if not pathlib.Path(log_path).exists():
        await update.message.reply_text("⚠️ Лог-файл не найден.")
        return

    # Показываем, что бот "загружает" файл
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    # Открываем и отправляем файл как документ
    with open(log_path, "rb") as f:
        await update.message.reply_document(InputFile(f), filename=log_path)