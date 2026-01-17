from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === SOZLAMALAR ===
TOKEN = "8341785424:AAHk6krDSn0PUy5G0ia-7BhbklGeukxMhS0"
ADMIN_ID =8439075898  # admin Telegram ID

users = {}

services_keyboard = ReplyKeyboardMarkup(
    [
        ["💻 Windows o‘rnatish", "🧹 Kompyuter tozalash"],
        ["🛠 Dastur o‘rnatish", "🔒 Virus tozalash"],
        ["📝 Boshqa xizmat"]
    ],
    resize_keyboard=True
)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users[user_id] = {"step": "name"}
    await update.message.reply_text("👤 Ism va familiyangizni kiriting:")

# Matnlar bilan ishlash
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    text = update.message.text

    if user_id not in users:
        await start(update, context)
        return

    step = users[user_id]["step"]

    # 1️⃣ Ism familiya
    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "service"
        await update.message.reply_text(
            "🛠 Kerakli xizmatni tanlang:",
            reply_markup=services_keyboard
        )

    # 2️⃣ Xizmat tanlash
    elif step == "service":
        if text == "📝 Boshqa xizmat":
            users[user_id]["step"] = "custom_service"
            await update.message.reply_text("✍️ Qanday xizmat kerakligini yozing:")
        else:
            users[user_id]["service"] = text
            users[user_id]["step"] = "message"
            await update.message.reply_text("📝 Muammo yoki xabaringizni yozing:")

    # 3️⃣ Boshqa xizmat nomi
    elif step == "custom_service":
        users[user_id]["service"] = text
        users[user_id]["step"] = "message"
        await update.message.reply_text("📝 Muammo yoki xabaringizni yozing:")

    # 4️⃣ Asosiy xabar
    elif step == "message":
        name = users[user_id]["name"]
        service = users[user_id]["service"]
        message = text

        # USERNAME olish
        username = user.username
        if username:
            username = "@" + username
        else:
            username = "mavjud emas"

        admin_text = (
            "📩 Yangi buyurtma!\n\n"
            f"👤 Ism: {name}\n"
            f"🛠 Xizmat: {service}\n"
            f"📝 Xabar: {message}\n"
            f"👤 Username: {username}"
        )

        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

        await update.message.reply_text(
            "✅ Buyurtmangiz yuborildi!\nTez orada siz bilan bog‘lanamiz 😊"
        )

        users[user_id]["step"] = "done"

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
