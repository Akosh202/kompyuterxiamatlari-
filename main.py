from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8341785424:AAHk6krDSn0PUy5G0ia-7BhbklGeukxMhS0"
ADMIN_ID = 8439075898

users = {}

services_keyboard = ReplyKeyboardMarkup(
    [
        ["💻 Windows o‘rnatish", "🧹 Kompyuter tozalash"],
        ["🛠 Dastur o‘rnatish", "🔒 Virus tozalash"],
        ["📝 Boshqa xizmat"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users[user_id] = {"step": "name"}
    await update.message.reply_text("👤 Ism va familiyangizni kiriting:")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in users:
        await start(update, context)
        return

    step = users[user_id]["step"]

    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "service"
        await update.message.reply_text(
            "🛠 Kerakli xizmatni tanlang:",
            reply_markup=services_keyboard
        )

    elif step == "service":
        if text == "📝 Boshqa xizmat":
            users[user_id]["step"] = "custom_service"
            await update.message.reply_text("✍️ Qanday xizmat kerakligini yozing:")
        else:
            users[user_id]["service"] = text
            users[user_id]["step"] = "message"
            await update.message.reply_text("📝 Muammo yoki xabaringizni yozing:")

    elif step == "custom_service":
        users[user_id]["service"] = text
        users[user_id]["step"] = "message"
        await update.message.reply_text("📝 Muammo yoki xabaringizni yozing:")

    elif step == "message":
        admin_text = (
            "📩 Yangi buyurtma!\n\n"
            f"👤 Ism: {users[user_id]['name']}\n"
            f"🛠 Xizmat: {users[user_id]['service']}\n"
            f"📝 Xabar: {text}\n"
            f"🆔 User ID: {user_id}"
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
