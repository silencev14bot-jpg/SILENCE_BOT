from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

import silenceAI
from telegram.access_gate import check_access, build_join_buttons
from telegram.watcher import watch_membership

BOT_TOKEN = "8479495792:AAHT7qgChZTL4bB2Ia4cHdPrbv-7oBuSAg0"  # <-- your bot token


# ===============================
# /start COMMAND
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    missing_channels, missing_groups = await check_access(
        context.bot,
        user.id
    )

    # ❌ NOT JOINED → LOCK
    if missing_channels or missing_groups:
        buttons = build_join_buttons(missing_channels, missing_groups)

        await update.message.reply_text(
            "🔒 **SILENCE 🜲 ACCESS REQUIRED**\n\n"
            "You must join all required channels & groups to use this bot.\n"
            "After joining, press /start again 🤍",
            reply_markup=buttons,
            parse_mode="Markdown",
        )
        return

    await update.message.reply_text(
    "✨ Welcome to SILENCE 🜲\n\n"
    "Access verified.\n"
    "You can now use commands or chat freely 🤍"
)


# ===============================
# NORMAL MESSAGE HANDLER
# ===============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""

    # 🔒 ACCESS CHECK
    missing_channels, missing_groups = await check_access(
        context.bot,
        user.id
    )

    if missing_channels or missing_groups:
        buttons = build_join_buttons(missing_channels, missing_groups)

        await update.message.reply_text(
            "🚫 **ACCESS LOCKED**\n\n"
            "You left a required channel or group.\n"
            "Rejoin to continue using SILENCE 🜲 🤍",
            reply_markup=buttons,
            parse_mode="Markdown",
        )
        return

    # ✅ ACCESS GRANTED → SILENCE CORE
    processed = silenceAI.Perception.process_input(text)

    if processed["intent"] == "command":
        parts = text[1:].split()
        cmd = parts[0]
        args = parts[1:]
        response = silenceAI.Commands.execute(
            str(user.id),
            cmd,
            *args
        )
    else:
        response = silenceAI.ResponseGenerator.generate(processed)

    await update.message.reply_text(str(response))


# ===============================
# BUTTON PAGINATION HANDLER
# ===============================
async def handle_gate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split(":")[1])
    user_id = query.from_user.id

    missing_channels, missing_groups = await check_access(
        context.bot,
        user_id
    )

    buttons = build_join_buttons(
        missing_channels,
        missing_groups,
        page=page
    )

    await query.edit_message_reply_markup(reply_markup=buttons)


# ===============================
# MAIN
# ===============================
def main():
    request = HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
    )

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_gate_callback, pattern="^gate:"))
    app.add_handler(ChatMemberHandler(watch_membership, ChatMemberHandler.CHAT_MEMBER))

    print("🤖 Telegram bot running…")
    app.run_polling()


if __name__ == "__main__":
    main()