import os
from telegram.ext import CommandHandler, Application, ContextTypes
from telegram import Update
from io import BytesIO

from utils.memory_google import save_memory_to_drive, create_drive_folder, load_memory_from_drive

# ID владельца
ADMIN_CHAT_ID = 839647871

# === Функция чтения текста из файла ===
def load_text_file(filename: str, fallback: str = "") -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception:
        return fallback

# Загружаем приветствие при старте бота
WELCOME_MESSAGE = load_text_file("utils/hello.txt", fallback=(
    "Привіт! Я AI-помічник типографії 🧠\n"
    "Знаю майже все про компанію та відповідаю на більшість питань.\n"
    "Можу звернутись до власника або з'єднати Вас напряму.\n"
    "Чим можу допомогти зараз?"
))

# === Обработчик команды /start ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

    user = update.effective_user
    message = (
        f"📥 Новий користувач:\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username or '—'}\n"
        f"Ім’я: {user.full_name}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

# === Обработчик команды /reply <user_id> <текст> ===
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("⛔ У Вас немає прав для цієї команди.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Приклад: /reply 123456789 Текст відповіді")
        return

    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=f"💬 Власник відповів:\n{reply_text}")
        await update.message.reply_text("✅ Відповідь надіслана.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# === Обработчик команды /save_test ===
async def save_test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    test_message = "🧪 Тестове повідомлення з команди /save_test"

    try:
        result = save_memory_to_drive(user_id, test_message)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка збереження: {e}")

# === Обработчик команды /create_folder_test ===
async def create_folder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        folder_id = create_drive_folder("SvitBotMemory")
        await update.message.reply_text(f"✅ Папка створена!\nID: `{folder_id}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка створення папки: {e}")

# === Обработчик команды /load_test ===
async def load_test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        content = load_memory_from_drive(user_id)

        if not content:
            await update.message.reply_text("ℹ️ Історія пуста.")
        elif len(content) < 3000:
            await update.message.reply_text(f"🧠 Памʼять:\n\n{content}")
        else:
            file_stream = BytesIO(content.encode("utf-8"))
            file_stream.name = f"user_{user_id}_memory.txt"
            await update.message.reply_document(document=file_stream, filename=file_stream.name)
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка при завантаженні: {e}")

# === Регистрация всех хендлеров ===
def add_handlers(application: Application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("reply", reply_command))
    application.add_handler(CommandHandler("save_test", save_test_command))
    application.add_handler(CommandHandler("create_folder_test", create_folder_command))
    application.add_handler(CommandHandler("load_test", load_test_command))
