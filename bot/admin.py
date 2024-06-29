from telegram import *
from telegram.ext import *

from web3 import Web3

from constants import bot, chains
from hooks import api, db, functions, tools


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            await update.message.reply_text(
                "/refund [generated wallet]\n"
                "/search [generated wallet]\n"
                "/view\n",
            parse_mode="Markdown"
            )

async def refund(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            address = " ".join(context.args)
            search = db.search_entry_by_address(address)
            if search:
                result = functions.transfer_balance(search["chain"], address, search["owner"], search["secret_key"])
                if result.startswith("Error"):
                    await update.message.reply_text(result)
                else:
                    chain_link = chains.chains[search["chain"]].scan_tx
                    await update.message.reply_text(f"Balance withdrawn\n\n{chain_link}{result}")
            else:
                await update.message.reply_text(
                    f"`{address}` Not found",
                parse_mode="Markdown"
                )


async def search(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            address = " ".join(context.args)
            if address == "":
                await update.message.reply_text("Provide address")
            else:
                entry = db.search_entry_by_address(address)
                if entry:
                    chain_web3 = chains.chains[entry["chain"]].w3
                    web3 = Web3(Web3.HTTPProvider(chain_web3))
                    balance_wei = web3.eth.get_balance(address)
                    balance = web3.from_wei(balance_wei, 'ether')

                    await update.message.reply_text(
                        f"User Name: {tools.escape_markdown(entry['user_name'])}\n"
                        f"User ID: {entry['user_id']}\n"
                        f"Submitted: {entry['timedate']}\n"
                        f"Current Balance: {int(balance)} {entry.upper()} ({entry['chain']})\n"
                        f"Address: `{entry['address']}`\n"
                        f"Key: `{entry['secret_key']}`\n",
                    parse_mode="Markdown",
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
                chain_native = chains.chains[entry["chain"]].token
                chain_web3 = chains.chains[entry["chain"]].w3
                web3 = Web3(Web3.HTTPProvider(chain_web3))
                balance_wei = web3.eth.get_balance(entry["address"])
                balance = web3.from_wei(balance_wei, 'ether')
                formatted_entry = (
                    f"User Name: {tools.escape_markdown(entry['user_name'])}\n"
                    f"User ID: {entry['user_id']}\n"
                    f"Submitted: {entry['timedate']}\n"
                    f"Current Balance: {int(balance)} {chain_native.upper()} ({entry['chain']})\n"
                    f"Address: `{entry['address']}`\n"
                    f"Key: `{entry['secret_key']}`\n"
                    f"-----------------------\n"
                )
                formatted_entries.append(formatted_entry)

            message = "".join(formatted_entries)
            
            await update.message.reply_text(
                message,
                parse_mode="Markdown"
            )