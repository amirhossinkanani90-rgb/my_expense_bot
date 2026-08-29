import json
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

FILE_NAME = "expenses.json"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        expenses = json.load(file)
else:
    expenses = []


def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ربات مدیریت هزینه\n\n"
        "دستورها:\n"
        "/add نام_هزینه مبلغ\n"
        "/list\n"
        "/total\n"
        "/clear"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "مثال:\n/add food 500"
        )
        return

    name = context.args[0]

    try:
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text("مبلغ باید عدد باشد.")
        return

    expenses.append([name, amount])
    save_data()

    await update.message.reply_text("✅ هزینه ثبت شد.")


async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not expenses:
        await update.message.reply_text("📋 هنوز هزینه‌ای ثبت نشده است.")
        return

    text = "📋 لیست هزینه‌ها:\n\n"

    for name, amount in expenses:
        text += f"• {name}: {amount}\n"

    await update.message.reply_text(text)


async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_amount = sum(item[1] for item in expenses)

    await update.message.reply_text(
        f"💰 مجموع هزینه‌ها: {total_amount}"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expenses.clear()
    save_data()

    await update.message.reply_text(
        "🗑️ همه هزینه‌ها حذف شدند."
    )


TOKEN = os.getenv("8996548170:AAEwBan6A6KmjG7X06nso8VBGACDWeWy5Cg")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", show_list))
app.add_handler(CommandHandler("total", total))
app.add_handler(CommandHandler("clear", clear))

app.run_polling()
