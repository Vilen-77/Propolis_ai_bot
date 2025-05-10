from telegram.ext import CommandHandler, Application
from telegram import Update
from telegram.ext import ContextTypes

# ID владельца
ADMIN_CHAT_ID = 839647871

# === Обработчик команды /start ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я AI-помічник типографії 🧠\n"
        "Знаю майже все про компанію та відповідаю на більшість питань.\n"
        "Можу звернутись до власника або з'єднати Вас напряму.\n"
        "Чим можу допомогти зараз?"
    )

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

# === Регистрация всех хендлеров ===
def add_handlers(application: Application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("reply", reply_command))
