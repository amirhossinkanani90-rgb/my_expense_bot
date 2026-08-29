import json
import os
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8996548170:AAEwBan6A6KmjG7X06nso8VBGACDWeWy5Cg"
FILE_NAME = "bookings.json"


def load_data():
    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


bookings = load_data()


def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(bookings, file, ensure_ascii=False, indent=4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "🤖 ربات نوبت‌دهی\n\n"
        "دستورها:\n"
        "/book نام شماره\n"
        "/mybooking\n"
        "/list\n"
        "/cancel\n\n"
        "مثال:\n"
        "/book Amir 09123456789"
    )

    await update.message.reply_text(message)


async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "مثال:\n/book Amir 09123456789"
        )
        return

    user_id = str(update.effective_user.id)
    name = context.args[0]
    phone = context.args[1]

    bookings[user_id] = {
        "name": name,
        "phone": phone,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    save_data()

    await update.message.reply_text("✅ نوبت ثبت شد.")


async def mybooking(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    if user_id not in bookings:
        await update.message.reply_text("❌ نوبتی پیدا نشد.")
        return

    booking = bookings[user_id]

    message = (
        f"👤 نام: {booking['name']}\n"
        f"📞 شماره: {booking['phone']}\n"
        f"🕒 زمان: {booking['time']}"
    )

    await update.message.reply_text(message)


async def list_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not bookings:
        await update.message.reply_text("❌ هیچ رزروی ثبت نشده است.")
        return

    message = "📋 همه رزروها:\n\n"

    for booking in bookings.values():
        message += (
            f"👤 {booking['name']}\n"
            f"📞 {booking['phone']}\n"
            f"🕒 {booking['time']}\n\n"
        )

    await update.message.reply_text(message)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    if user_id not in bookings:
        await update.message.reply_text("❌ رزروی وجود ندارد.")
        return

    del bookings[user_id]

    save_data()

    await update.message.reply_text("🗑️ رزرو حذف شد.")


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("book", book))
    app.add_handler(CommandHandler("mybooking", mybooking))
    app.add_handler(CommandHandler("list", list_bookings))
    app.add_handler(CommandHandler("cancel", cancel))

    print("ربات اجرا شد...")

    app.run_polling()


if __name__ == "__main__":
    main()