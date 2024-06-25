from telegram import *
from telegram.ext import *
from web3 import Web3

from constants import chains, bot
from hooks import api, db, deployments

chainscan = api.ChainScan()

async def test(update: Update, context: CallbackContext) -> int:
    return


async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    user_name = user.username or f"{user.first_name} {user.last_name}"
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            f"*THIS IS BETA BOT, DO NOT SEND ANY FUNDS TO MAINNET WALLETS, THEY WILL BE LOST\n*\n"
            f"Welcome {api.escape_markdown(user_name)} to {api.escape_markdown(bot.BOT_NAME)}\n\n"
            f"Create a token and Launch an Xchange pair in minutes, with upto {bot.LOAN_AMOUNT} ETH liquidity for {bot.LOAN_FEE} ETH\n\n"
            "Loan will be repaid after 7 days via pair liquidity unless its paid back sooner!\n\n"
            f"{bot.LOAN_DEPOSIT} ETH liquidation deposit will be returned to liquidator upon loan completion/liquidation\n\n"
            "use /launch to start your project now!",
        parse_mode="Markdown"
        )


async def reset(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        delete_text = db.delete_entry_by_user_id(user_id)
        if delete_text:
            await update.message.reply_text(
                f"Project reset, use /launch to start"
            )
        else:
            await update.message.reply_text("No projects waiting, please use /launch to start")


async def status(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            chain_web3 = chains.chains[status_text["chain"].lower()].w3
            web3 = Web3(Web3.HTTPProvider(chain_web3))
            balance_wei = web3.eth.get_balance(status_text["address"])
            balance = web3.from_wei(balance_wei, 'ether')
            balance_str = format(balance, '.18f')
            if status_text["complete"] == 0:
                if float(balance) >= float(bot.LOAN_FEE):
                        button = InlineKeyboardMarkup(
                                [
                                    [InlineKeyboardButton(text="LAUNCH", callback_data="launch")],
                                ]
                            )
                        message = "Ready to launch, hit the button below!"
                        header = "*LAUNCH STATUS - READY*"
                        was_will_be = "will be"
                else:
                    message = f"Fund `{status_text["address"]}` with {bot.LOAN_FEE} ETH or use /reset to clear this launch"
                    header = "*LAUNCH STATUS - WAITING*"
                    was_will_be = "will be"
                    button = ""
            else:
                button = ""
                message = f"Use /reset to clear this launch"
                header = "*LAUNCH STATUS - CONFIRMED*"
                was_will_be = "was"

            team_tokens = int(status_text["supply"]) * (int(status_text["amount"]) / 100)
            liquidity_tokens = int(status_text["supply"]) - team_tokens

            price_eth = int(status_text["loan"]) / liquidity_tokens
            price_usd = price_eth * chainscan.get_native_price(status_text["chain"].lower()) * 2
            market_cap_usd = price_usd * int(status_text["supply"]) * 2

            await update.message.reply_text(
                    f"{header}\n\n"
                    f"{status_text["ticker"]} ({status_text["chain"]})\n\n"
                    f"Name: {status_text["name"]}\n"
                    f"Total Supply: {status_text["supply"]}\n"
                    f"Team Supply: {status_text["amount"]}%\n"
                    f"Loan Amount: {status_text["loan"]} ETH\n\n"
                    f"Launch Token Price: ${price_usd:.8f}\n"
                    f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
                    f"Ownership {was_will_be} transfered to:\n`{status_text["owner"]}`\n\n"
                    f"Current Deployer Wallet Balance:\n"
                    f"{balance_str} ETH\n\n"
                    f"{message}",
                parse_mode="Markdown",
                reply_markup=button
            )
        else:
            await update.message.reply_text("No projects waiting, please use /launch to start")


async def withdraw(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            deployments.transfer_balance(status_text["chain"].lower(), status_text["address"], status_text["owner"], status_text["secret_key"])



