from telegram import *
from telegram.ext import *
from web3 import Web3
from eth_account import Account
from datetime import datetime

from hooks import api, db
from constants import bot, urls, bot

chainscan = api.ChainScan()


async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    user_name = user.username or f"{user.first_name} {user.last_name}"
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            f"*THIS IS BETA BOT, DO NOT SEND ANY FUNDS, THEY WILL BE LOST\n*\n"
            f"Welcome {api.escape_markdown(user_name)} to {api.escape_markdown(bot.BOT_NAME)}\n\n"
            f"Launch an Xchange pair in minutes, with {bot.LOAN_AMOUNT} ETH liquidity for {bot.LOAN_FEE} ETH\n\n"
            "Loan will be repaid after 7 days via pair liquidity unless its paid back sooner!\n\n"
            f"{bot.LOAN_DEPOSIT} ETH liquididation deposit will be returned upon loan completion\n\n"
            "use /launch to launch your project now!",
        parse_mode="Markdown"
        )

async def reset(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        delete_text = db.delete_entry_by_user_id(user_id)
        if delete_text:
            await update.message.reply_text(
                f"Launch reset, use /launch to start"
            )
        else:
            await update.message.reply_text("No launches waiting, please use /launch to start")

async def status(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            balance = chainscan.get_native_balance(status_text["address"], status_text["chain"].lower())
            if balance >= bot.LOAN_FEE:
                launch_message = "Ready to deploy, use /deploy to continue!"
            else:
                launch_message = f"Fund `{status_text["address"]}` with {bot.LOAN_FEE} ETH or use /reset to clear this launch\n\n"
            await update.message.reply_text(
                f"Currently awaiting launch for {status_text["ticker"]} ({status_text["chain"]})\n\n"
                f"Name: {status_text["name"]}\n"
                f"Supply: {status_text["supply"]}\n"
                f"TG Portal: {status_text["portal"]}\n"
                f"Website: {status_text["website"]}\n\n"
                f"Current Balance:\n"
                f"{balance} ETH\n\n"
                f"Ownership will be transfered to:\n{status_text["owner"]}\n\n"
                f"{launch_message}",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("No launches waiting, please use /launch to start")


async def deploy(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            balance = chainscan.get_native_balance(status_text["address"], status_text["chain"].lower())
            if balance >= bot.LOAN_FEE:
                 await update.message.reply_text(
                f"Deploying {status_text["ticker"]} ({status_text["chain"]})\n\n"
                f"Name: {status_text["name"]}\n"
                f"Supply: {status_text["supply"]}\n"
                f"TG Portal: {status_text["portal"]}\n"
                f"Website: {status_text["website"]}\n\n"
                f"Ownership will be transfered to:\n{status_text["owner"]}\n\n",
                parse_mode="Markdown"
            )
            #### DEPLOY HERE ###
            else:
                await update.message.reply_text(
                    f"Currently awaiting launch for {status_text["ticker"]} ({status_text["chain"]})\n\n"
                    f"Name: {status_text["name"]}\n"
                    f"Supply: {status_text["supply"]}\n"
                    f"TG Portal: {status_text["portal"]}\n"
                    f"Website: {status_text["website"]}\n\n"
                    f"Current Balance:\n"
                    f"{balance} ETH\n\n"
                    f"Ownership will be transfered to:\n{status_text["owner"]}\n\n"
                    f"Fund `{status_text["address"]}` with {bot.LOAN_FEE} ETH or use /reset to clear this launch\n\n",
                    parse_mode="Markdown"
                )
        else:
            await update.message.reply_text("No deployments waiting, please use /launch to start")
