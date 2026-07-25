from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
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
                    "💬 Chat Now",
                    url=girl["bot"]
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


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
