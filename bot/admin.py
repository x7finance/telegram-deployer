from telegram import *
from telegram.ext import *

from datetime import datetime, timedelta

from constants import bot, chains
from hooks import db, tools


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            await update.message.reply_text(
                "/delete [user_id]\n"
                "/search [user_id]\n"
                "/view\n",
            parse_mode="Markdown"
            )


async def delete(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            id = " ".join(context.args)
            delete_result = db.delete_entry(id)

            if delete_result:
                await update.message.reply_text(
                    f"{id} has been deleted.",
                parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    f"{id} not found.",
                parse_mode="Markdown"
                )



async def search(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            id = " ".join(context.args)
            if id == "":
                await update.message.reply_text("Provide user ID")
            else:
                entry = db.search_entry(id)
                if entry:
                    chain_info = chains.chains[entry["chain"]]
                    balance_wei = chain_info.w3.eth.get_balance(entry['address'])
                    balance = chain_info.w3.from_wei(balance_wei, 'ether')
                    if entry['complete'] == 1:
                        status = "Deployed"
                    else:
                        status = "Awaiting Deployment"
                    await update.message.reply_text(
                        f"User Name:\n`{tools.escape_markdown(entry['user_name'])}`\n"
                        f"User ID:\n`{entry['user_id']}`\n"
                        f"Owner:\n`{entry['owner']}`\n"
                        f"Staus:\n`{status}`\n"
                        f"Submitted:\n`{entry['timedate']}`\n"
                        f"Current Balance:\n`{balance} ({entry['chain'].upper()})`\n"
                        f"Address:\n`{entry['address']}`\n"
                        f"Key:\n`{entry['secret_key']}`\n\n",
                    parse_mode="Markdown",
                    )
                else:
                    await update.message.reply_text(
                        f"Nothing found for `{id}`",
                    parse_mode="Markdown"
                    )


async def view(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        if user_id in bot.ADMINS:
            entries = db.get_all_entries()

            if not entries:
                await update.message.reply_text("No entries found.")
                return ConversationHandler.END

            one_month_ago = datetime.now() - timedelta(days=30)
            formatted_entries = []
            for entry in entries:
                chain_info = chains.chains[entry["chain"]]
                balance_wei = chain_info.w3.eth.get_balance(entry["address"])
                balance = chain_info.w3.from_wei(balance_wei, 'ether')
                
                entry_date = entry["timedate"]
                if isinstance(entry_date, str):
                    entry_date = datetime.strptime(entry["timedate"], '%Y-%m-%d %H:%M:%S')

                if entry_date < one_month_ago and balance < 0.001:
                    db.delete_entry(entry["user_id"])
                    continue
                
                if entry['complete'] == 1:
                    status = "Deployed"
                else:
                    status = "Awaiting Deployment"
                formatted_entry = (
                    f"User Name:\n`{tools.escape_markdown(entry['user_name'])}`\n"
                    f"User ID:\n`{entry['user_id']}`\n"
                    f"Owner:\n`{entry['owner']}`\n"
                    f"Status:\n`{status}`\n"
                    f"Submitted:\n`{entry['timedate']}`\n"
                    f"Current Balance:\n`{balance:.7f} ({entry['chain'].upper()})`\n"
                    f"Address:\n`{entry['address']}`\n"
                    f"Key:\n`{entry['secret_key']}`\n"
                    f"-----------------------\n"
                )
                formatted_entries.append(formatted_entry)

            if formatted_entries:
                message = "".join(formatted_entries)
                message_chunks = tools.split_message(message, max_length=4096)
                for chunk in message_chunks:
                    await update.message.reply_text(
                        chunk,
                        parse_mode="Markdown"
                    )
            else:
                await update.message.reply_text("No valid entries remaining after cleaning.")
