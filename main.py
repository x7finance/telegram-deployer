from telegram import *
from telegram.ext import *

import os, sentry_sdk

from bot import admin, commands, launch

application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

sentry_sdk.init(
    dsn = os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0
)


async def error(update: Update, context: CallbackContext):
    if update is None:
        return
    if update.edited_message is not None:
        return
    else:
        message: Message = update.message
        if message is not None and message.text is not None:
            await update.message.reply_text(
                "Error while loading data, please try again"
            )
            print({context.error})
            sentry_sdk.capture_exception(
                Exception(f"{message.text} caused error: {context.error}")
                )
        else:
            sentry_sdk.capture_exception(
                Exception(
                    f"Error occurred without a valid message: {context.error}"
                )
            )


if __name__ == "__main__":
    application.add_error_handler(error)
    application.add_handler(CommandHandler("test", commands.test))

    ## ADMIN ##
    application.add_handler(CommandHandler("admin", admin.command))
    application.add_handler(CommandHandler("delete", admin.delete))
    application.add_handler(CommandHandler("search", admin.search))
    application.add_handler(CommandHandler("view", admin.view))

    ## COMANDS ##
    application.add_handler(CommandHandler("id", commands.id))
    application.add_handler(CommandHandler("reset", commands.reset))
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("status", commands.status))
    application.add_handler(CommandHandler("withdraw", commands.withdraw))
    launch_handler = ConversationHandler(
        entry_points=[CommandHandler('launch', launch.command)],
        states={
            launch.STAGE_CHAIN: [CallbackQueryHandler(launch.stage_chain, pattern='^chain_')],
            launch.STAGE_TICKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_ticker)],
            launch.STAGE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_name)],
            launch.STAGE_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_description)],
            launch.STAGE_TWITTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_twitter)],
            launch.STAGE_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_telegram)],
            launch.STAGE_WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_website)],
            launch.STAGE_BUY_TAX: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_buy_tax)],
            launch.STAGE_SELL_TAX: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_sell_tax)],
            launch.STAGE_SUPPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_supply)],
            launch.STAGE_AMOUNT: [CallbackQueryHandler(launch.stage_amount, pattern='^amount_')],
            launch.STAGE_LOAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_loan)],
            launch.STAGE_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_duration)],
            launch.STAGE_CONTRIBUTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_contribute)],
            launch.STAGE_OWNER: [MessageHandler(filters.TEXT & ~filters.COMMAND, launch.stage_owner)],
            launch.STAGE_CONFIRM: [CallbackQueryHandler(launch.stage_confirm, pattern='^confirm_')],
        },
        fallbacks=[CommandHandler('cancel', launch.cancel)],
    )
    application.add_handler(launch_handler)
    application.add_handler(CallbackQueryHandler(commands.reset_callback, pattern='^reset_'))
    application.add_handler(CallbackQueryHandler(launch.with_loan, pattern='^launch_with_loan$'))
    application.add_handler(CallbackQueryHandler(launch.without_loan, pattern='^launch_without_loan$'))

    ## START ##
    application.run_polling(allowed_updates=Update.ALL_TYPES)
