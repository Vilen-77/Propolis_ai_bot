from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder
from utils.config import TOKEN, WEBHOOK_URL
from modules.commands import add_handlers  # теперь /start берём из модуля

app = FastAPI()

# Создаём Telegram Application
bot_app = ApplicationBuilder().token(TOKEN).build()

@app.on_event("startup")
async def startup_event():
    await bot_app.initialize()           # обязательно для вебхуков!
    add_handlers(bot_app)                # подключаем все команды
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)

@app.on_event("shutdown")
async def shutdown_event():
    await bot_app.shutdown()

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status": "ok"}
