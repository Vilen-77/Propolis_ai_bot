import os  # Импортируем модуль для работы с переменными окружения

# Получаем токен Telegram-бота из переменной окружения
# В Render ты добавляешь TELEGRAM_TOKEN в разделе Environment
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Получаем URL вебхука, на который Telegram будет отправлять сообщения
# Пример: https://название-проекта.onrender.com/
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Проверка: если переменные не заданы — можно будет вывести ошибку при запуске (опционально)
if not TOKEN:
    raise ValueError("Переменная окружения TELEGRAM_TOKEN не найдена!")

if not WEBHOOK_URL:
    raise ValueError("Переменная окружения WEBHOOK_URL не найдена!")
