from telegram import Message, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

import os
import sentry_sdk
from telegram.warnings import PTBUserWarning
from warnings import filterwarnings

from bot import callbacks, conversations
from bot.commands import admin, general
from utils import tools
from services import get_dbmanager

db = get_dbmanager()

filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)

application = (
    Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
)

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update is None:
        return

    if update.callback_query is not None:
        try:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                "An error occurred, please try again."
            )
        except Exception:
            await context.bot.send_message(
                chat_id=update.callback_query.message.chat_id,
                text="An error occurred, please try again.",
            )
        print({context.error})
        sentry_sdk.capture_exception(
            Exception(f"CallbackQuery caused error: {context.error}")
        )
        return

    if update.edited_message is not None:
        return

    message: Message = update.message
    if message is not None and message.text is not None:
        await message.reply_text("An error occurred, please try again.")
        print({context.error})
        sentry_sdk.capture_exception(
            Exception(f"{message.text} caused error: {context.error}")
        )
    else:
        await context.bot.send_message(
            chat_id=message.chat_id if message else None,
            text="An error occurred, please try again.",
        )
        print({context.error})
        sentry_sdk.capture_exception(
            Exception(
                f"Error occurred without a valid message: {context.error}"
            )
        )


def init_bot():
    application.add_error_handler(error)

    for handler in conversations.HANDLERS:
        application.add_handler(
            ConversationHandler(
                entry_points=handler["entry_points"],
                states=handler["states"],
                fallbacks=handler.get(
                    "fallbacks",
                    [CommandHandler("cancel", conversations.cancel)],
                ),
            )
        )

    for cmd, handler, _ in admin.HANDLERS:
        application.add_handler(CommandHandler(cmd, handler))

    for cmd, handler, _ in general.HANDLERS:
        if isinstance(cmd, list):
            for alias in cmd:
                application.add_handler(CommandHandler(alias, handler))
        else:
            application.add_handler(CommandHandler(cmd, handler))

    for handler, pattern in callbacks.HANDLERS:
        application.add_handler(CallbackQueryHandler(handler, pattern=pattern))

    print("✅ Bot initialized")


async def post_init(application: Application):
    if not tools.is_local():
        print("✅ Bot Running on server")

        print(await tools.update_bot_commands())
        print(await tools.set_reminders(application))

    else:
        print("✅ Bot Running locally")


if __name__ == "__main__":
    init_bot()
    application.post_init = post_init
    application.run_polling(allowed_updates=Update.ALL_TYPES)
