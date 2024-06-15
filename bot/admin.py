from telegram import *
from telegram.ext import *

from datetime import timedelta

from constants import bot, chains
from hooks import api, db


chainscan = api.ChainScan()


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            await update.message.reply_text(
                f"/search [generated wallet]",
            parse_mode="Markdown"
            )


async def search(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            address = " ".join(context.args)
            status_text = db.search_entry_by_address(address)
            if status_text:
                if status_text["chain"].lower() in chains.chains:
                    chain_scan = chains.chains[status_text["chain"].lower()].scan_address
                balance = chainscan.get_native_balance(address, status_text["chain"].lower())
                expires = status_text["timedate"] + timedelta(hours=bot.DELETE_HOURS)
                await update.message.reply_text(
                    f"`{address}`\n"
                    f"User ID: {status_text["user_id"]}\n"
                    f"User Name: {status_text["user_name"]}\n"
                    f"Opened: {status_text["timedate"]}\n"
                    f"Expires: {expires}\n"
                    f"Secret Key: `{status_text["secret_key"]}`\n\n"
                    f"{status_text["chain"]}\n"
                    f"Ticker: {status_text["ticker"]}\n"
                    f"Name: {status_text["name"]}\n"
                    f"Supply: {status_text["supply"]}\n"
                    f"TG Portal: {status_text["portal"]}\n"
                    f"Website: {status_text["website"]}\n\n"
                    f"Current Balance:\n"
                    f"{balance} ETH\n\n"
                    f"Ownership will be transfered to:\n{status_text["owner"]}\n\n",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Wallet Link",
                                url=f"{chain_scan}{address}",
                            )
                        ],
                    ]
                ),
                        )
            else:
                 await update.message.reply_text(f"Nothing found for `{address}`",
            parse_mode="Markdown"
            )