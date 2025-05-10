# Импортируем нужные классы и функции из библиотеки python-telegram-bot

from telegram import Update  # Update — объект, представляющий сообщение пользователя
from telegram.ext import Application, CommandHandler, ContextTypes  # Классы для запуска и управления ботом

import os  # Импортируем os для доступа к переменным окружения

# Импортируем функцию для загрузки файлов на Google Диск
# Предполагается, что upload_to_drive.py находится в папке "modules"
from modules.upload_to_drive import upload_to_drive

# Получаем токен Telegram бота из переменной окружения
# Этот токен ты добавишь на Render или укажешь в .env-файле
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Указываем Telegram-username администратора (без @)
# Только этот пользователь сможет вызывать админ-команды (например, /uploadlog)
ADMIN_USERNAME = "Vilen77"

# --------------------------------------
# Команда /start — приветствие
# --------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username

    # Если пользователь — админ
    if username == ADMIN_USERNAME:
        await update.message.reply_text("Привет, админ! Бот работает.")
    else:
        # Приветствие обычного пользователя
        await update.message.reply_text("Здравствуйте! Я виртуальный помощник. Чем могу помочь?")

        # Загружаем лог-файл на Google Диск (автоматически)
        try:
            upload_to_drive("log_stea_verde.txt")
        except Exception as e:
            print(f"Ошибка при загрузке лога: {e}")

# --------------------------------------
# Команда /uploadlog — загрузка файла на Google Диск
# --------------------------------------

async def uploadlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем username пользователя, который вызвал команду
    username = update.effective_user.username

    # Разрешаем выполнять команду только администратору
    if username != ADMIN_USERNAME:
        await update.message.reply_text("⛔ У Вас нет доступа к этой команде.")
        return

    # Указываем имя файла, который хотим загрузить (лог)
    filename = "log_stea_verde.txt"

    try:
        # Загружаем файл на Google Диск через функцию из upload_to_drive.py
        upload_to_drive(filename)

        # Отправляем подтверждение в Telegram
        await update.message.reply_text(f"✅ Файл {filename} успешно загружен на Google Диск.")
    except Exception as e:
        # Если произошла ошибка — сообщаем об этом админу
        await update.message.reply_text(f"❌ Ошибка при загрузке файла: {e}")

# --------------------------------------
# Главная функция — запуск бота
# --------------------------------------

def main():
    # Создаём Telegram-приложение с указанным токеном
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))           # команда /start
    app.add_handler(CommandHandler("uploadlog", uploadlog))   # команда /uploadlog

    # Запускаем бота в режиме "опроса" (проверка на новые сообщения)
    app.run_polling()

# --------------------------------------
# Запуск бота (только если файл запускается напрямую)
# --------------------------------------

if __name__ == "__main__":
    main()
