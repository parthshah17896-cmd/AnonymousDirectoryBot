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
from database import (
    init_db,
    user_exists,
    save_selection,
    get_selection
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    if user_exists(telegram_id):

        selected_name, selected_bot = get_selection(telegram_id)

        keyboard = [[
            InlineKeyboardButton(
                "🚀 Continue Chat",
                url=selected_bot
            )
        ]]

        await update.message.reply_text(
            f"❤️ Welcome back!\n\n"
            f"You have already selected *{selected_name}*.\n\n"
            "Use the button below to continue chatting.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return
        
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

    telegram_id = query.from_user.id

    # Check if the user has already selected a profile
    if user_exists(telegram_id):

        selected_name, selected_bot = get_selection(telegram_id)

        keyboard = [[
            InlineKeyboardButton(
                "🚀 Continue Chat",
                url=selected_bot
            )
        ]]

        await query.edit_message_caption(
            caption=(
                f"❌ You have already selected *{selected_name}*.\n\n"
                "You cannot select another profile."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    profile_id = int(query.data.split("_")[1])

    girl = next(
        (g for g in profiles if g["id"] == profile_id),
        None
    )

    if girl is None:

        await query.answer(
            "Profile not found.",
            show_alert=True
        )

        return

    save_selection(
        telegram_id,
        girl["name"],
        girl["bot"]
    )

    keyboard = [[
        InlineKeyboardButton(
            "🚀 Open Chat",
            url=girl["bot"]
        )
    ]]

    await query.edit_message_caption(
        caption=(
            f"✅ *Selection Confirmed*\n\n"
            f"You selected ❤️ *{girl['name']}*\n\n"
            "This choice cannot be changed."
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():

    init_db()   # Creates users.db and the users table if they don't exist
    
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select_profile))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
