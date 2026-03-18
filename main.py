from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import io

TOKEN = "8761556951:AAF44rheez1rpLeUt3VwbQdZtQbSsI2ZIMQ"
ADMIN_ID = 8439075898

# MENU
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🤖 Bot yaratish", callback_data="bot")],
        [InlineKeyboardButton("🌐 Sayt yaratish", callback_data="site")],
        [InlineKeyboardButton("📂 Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("📝 Buyurtma berish", callback_data="order")],
        [InlineKeyboardButton("📩 Admin bilan bog‘lanish", callback_data="admin")]
    ]
    return InlineKeyboardMarkup(keyboard)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men sizga professional xizmatlar taklif qilaman.\n\nXizmatni tanlang 👇",
        reply_markup=main_menu()
    )

# BUTTON BOSILGANDA
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "bot":
        await query.message.reply_text(
            "🤖 Telegram bot yasab beraman!\n\n"
            "✔ Avto javob\n✔ To‘lov tizimi\n✔ Admin panel\n\n"
            "Narx: 150k dan\n\n"
            "Buyurtma berish uchun pastdagi tugmani bosing 👇"
        )

    elif query.data == "site":
        await query.message.reply_text(
            "🌐 Website yasab beraman!\n\n"
            "✔ Landing page\n✔ Biznes sayt\n✔ Tez va chiroyli dizayn\n\n"
            "Narx: 200k dan\n\n"
            "Buyurtma berish uchun menyudan foydalaning 👇"
        )

    elif query.data == "portfolio":
        await query.message.reply_text(
            "📂 Mening ishlarim:\n\n"
            "🌐 https://sening-sayting1.netlify.app\n"
            "🌐 https://sening-sayting2.netlify.app\n\n"
            "🤖 https://t.me/sen_yasagan_bot\n"
        )

    elif query.data == "order":
        await query.message.reply_text("📝 Ismingizni yozing:")
        context.user_data["step"] = "name"

    elif query.data == "admin":
        await query.message.reply_text("✍️ Xabaringizni yozing:")
        context.user_data["step"] = "admin_message"

# MESSAGE (FORMA VA ADMIN)
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text if update.message.text else None

    # BUYURTMA FORMASI
    if context.user_data.get("step") == "name":
        context.user_data["name"] = text
        await update.message.reply_text("📞 Telefon raqamingizni yozing:")
        context.user_data["step"] = "phone"

    elif context.user_data.get("step") == "phone":
        context.user_data["phone"] = text
        await update.message.reply_text("💼 Qaysi xizmat kerak? (bot / sayt)")
        context.user_data["step"] = "service"

    elif context.user_data.get("step") == "service":
        name = context.user_data["name"]
        phone = context.user_data["phone"]

        # ADMINGA YUBORISH
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 BUYURTMA:\n👤 {name}\n📞 {phone}\n💼 {text}"
        )

        await update.message.reply_text("✅ Buyurtmangiz yuborildi! Tez orada bog‘lanamiz.")
        context.user_data.clear()

    # ADMIN MESSAGE
    elif context.user_data.get("step") == "admin_message":
        user = update.message.from_user

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Xabar:\n👤 {user.first_name}\n🆔 {user.id}\n\n{text}"
        )

        await update.message.reply_text("✅ Xabaringiz yuborildi!")
        context.user_data.clear()

# APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT, message))

app.run_polling()
