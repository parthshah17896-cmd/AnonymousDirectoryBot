from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import BOT_TOKEN
from profiles import profiles


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💕 *Welcome to Anonymous Chat Directory*\n\n"
        "Browse the profiles below.\n"
        "Tap *Chat Now* to start chatting anonymously.",
        parse_mode="Markdown"
    )

    for girl in profiles:

        keyboard = [
            [
                InlineKeyboardButton(
                    f"💬 Select {girl['name']}",
                    callback_data=f"select_{girl['id']}"
                )
            ]
        ]

        text = (
            f"👩 *{girl['name']}*\n\n"
            f"🎂 Age: {girl['age']}\n"
            f"💍 Status: {girl['status']}\n"
            f"🌍 Country: {girl['country']}\n\n"
            f"📝 {girl['about']}"
        )

        with open(girl["photo"], "rb") as photo:

            await update.message.reply_photo(
                photo=photo,
                caption=text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

async def select_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    print(data)

    # Database check will go here later


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select_profile))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
