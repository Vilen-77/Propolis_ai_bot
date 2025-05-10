# Импортируем FastAPI — фреймворк, на базе которого будет работать наш веб-сервер
from fastapi import FastAPI, Request

# Импортируем необходимые классы и функции из библиотеки python-telegram-bot
from telegram import Update  # Update — структура входящего сообщения от Telegram
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Импортируем наш токен и URL вебхука из файла конфигурации
from utils.config import TOKEN, WEBHOOK_URL

# Создаём FastAPI-приложение — это точка входа для Telegram webhook
app = FastAPI()

# Создаём Telegram Application (бота) через ApplicationBuilder
bot_app = ApplicationBuilder().token(TOKEN).build()


# === Обработчик команды /start ===
# Эта функция вызывается, когда пользователь отправляет /start боту
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Telegram-бот, подключённый через вебхук 🚀")


# === Регистрируем обработчик команды в приложении бота ===
# Мы говорим боту: если получаешь /start, вызывай функцию start()
bot_app.add_handler(CommandHandler("start", start))


# === Обработка входящих запросов от Telegram (вебхук) ===
@app.post("/")
async def webhook(request: Request):
    # Получаем тело запроса от Telegram в формате JSON
    data = await request.json()

    # Преобразуем JSON-данные в объект Update (структура Telegram)
    update = Update.de_json(data, bot_app.bot)

    # Отправляем Update в приложение Telegram-бота на обработку
    await bot_app.process_update(update)

    # Возвращаем Telegram'у статус "всё ок"
    return {"status": "ok"}


# === Событие при старте FastAPI-приложения ===
@app.on_event("startup")
async def startup_event():
    # Устанавливаем вебхук — Telegram будет отправлять сообщения на наш сервер
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)


# === Событие при остановке FastAPI-приложения ===
@app.on_event("shutdown")
async def shutdown_event():
    # Корректно завершаем работу приложения Telegram-бота
    await bot_app.shutdown()
