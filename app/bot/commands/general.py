from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import conversations
from constants.bot import settings
from constants.protocol import chains
from utils import onchain, tools
from services import get_dbmanager, get_etherscan

db = get_dbmanager()
etherscan = get_etherscan()


async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            f"{update.effective_user.username}, Your user ID is: `{update.effective_user.id}`",
            parse_mode="Markdown",
        )


async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conversations.start_launch


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = await db.search_entry(user_id)

        if not status_text:
            await update.message.reply_text(
                "No projects waiting, please use /launch to start"
            )
            return
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="reset_yes"),
            InlineKeyboardButton("No", callback_data="reset_no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Are you sure you want to reset your project?\n\nPlease ensure you have no remaining "
        "funds in the designated deployer address or you have saved the address and private "
        "key\n\n*This action cannot be undone*",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.username or f"{user.first_name} {user.last_name}"
    chat_type = update.message.chat.type
    count = await db.count_launches()
    _, loan_fees = await tools.generate_loan_terms("base", 1)
    if chat_type == "private":
        await update.message.reply_text(
            f"Welcome to {tools.escape_markdown(settings.BOT_NAME)}, {tools.escape_markdown(user_name)}!\n"
            f"Your gateway to creating and launching tokens in just minutes.\n\n"
            f"*Here's what you can do:*\n"
            "- Launch a Token: Seamlessly create and deploy your token and trade instantly.\n"
            f"- Borrow Liquidity on Xchange: {loan_fees}\n"
            f"- Launch Instantly on Uniswap for 1% of token supply\n\n"
            "*Loan Terms:*\n"
            "- Choose your preferred loan duration. If unpaid by the expiry date, "
            "repayment will occur through pair liquidity.\n"
            f"- Refundable Deposit: The {settings.LIQUIDATION_DEPOSIT} ETH liquidation deposit is fully "
            "returned once your loan is settled.\n\n"
            f"Join the innovators—{count} tokens launched and counting!\n\n"
            "*Ready to launch your project?\n*"
            "use /launch to start your project now!",
            parse_mode="Markdown",
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    user_id = update.effective_user.id
    status_text = await db.search_entry(user_id)

    if not status_text:
        await update.message.reply_text(
            "No projects waiting, please use /launch to start"
        )
        return

    chain_info = await chains.get_chain_info(status_text["chain"])
    balance_wei = await chain_info.w3.eth.get_balance(status_text["address"])
    balance = chain_info.w3.from_wei(balance_wei, "ether")
    balance_str = format(balance, ".18f")

    if status_text["complete"] == 0:
        if status_text["dex"] == "xchange":
            token_text = (
                f"Description: {status_text['description']}\n"
                f"Twitter: {status_text['twitter']}\n"
                f"Telegram: {status_text['telegram']}\n"
                f"Website: {status_text['website']}\n"
            )
            if not status_text["loan"]:
                callback_data = "launch_without_loan"
                gas_estimate = await onchain.estimate_gas_without_loan(
                    status_text["chain"],
                    status_text["name"],
                    status_text["ticker"],
                    int(status_text["supply"]),
                    int(status_text["percent"]),
                    status_text["buy_tax"],
                    status_text["sell_tax"],
                    status_text["owner"],
                    int(status_text["fee"]),
                )
            else:
                callback_data = "launch_with_loan"
                gas_estimate = await onchain.estimate_gas_with_loan(
                    status_text["chain"],
                    status_text["name"],
                    status_text["ticker"],
                    int(status_text["supply"]),
                    int(status_text["percent"]),
                    status_text["buy_tax"],
                    status_text["sell_tax"],
                    chain_info.w3.to_wei(status_text["loan"], "ether"),
                    int(status_text["duration"]) * 60 * 60 * 24,
                    status_text["owner"],
                    int(status_text["fee"]),
                )
        else:
            token_text = ""
            callback_data = "launch_uniswap"
            gas_estimate = onchain.estimate_gas_uniswap(
                status_text["chain"],
                status_text["name"],
                status_text["ticker"],
                status_text["supply"],
                status_text["percent"],
                status_text["buy_tax"],
                status_text["sell_tax"],
                status_text["owner"],
                int(status_text["fee"]),
            )

        total_cost = int(status_text["fee"]) + gas_estimate
        if balance_wei >= total_cost:
            button = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="LAUNCH", callback_data=callback_data
                        )
                    ]
                ]
            )
            message = "Ready to launch, hit the button below!"
            header = f"*{status_text['dex'].upper()} ({status_text['chain'].upper()}) LAUNCH STATUS - READY*"
            was_will_be = "will be"
        else:
            button = ""
            message = (
                f"On {chain_info.name} send {round(chain_info.w3.from_wei(total_cost, 'ether'), 6)} "
                f"{chain_info.native.upper()} (This includes gas fees) to:\n"
                f"`{status_text['address']}`\n\n"
                "Any fees not used will be returned to the wallet you designated as owner at deployment.\n\n"
                "use /withdraw to return any un-used funds\n"
                "use /reset to clear this launch"
            )
            header = f"*{status_text['dex'].upper()} ({status_text['chain'].upper()}) LAUNCH STATUS - WAITING*"
            was_will_be = "will be"
    else:
        token_text = (
            (
                f"Description: {status_text['description']}\n"
                f"Twitter: {status_text['twitter']}\n"
                f"Telegram: {status_text['telegram']}\n"
                f"Website: {status_text['website']}\n"
            )
            if status_text["dex"] == "xchange"
            else ""
        )
        button = ""
        message = "use /withdraw to return any un-used funds\nuse /reset to clear this launch"
        header = f"*{status_text['dex'].upper()} ({status_text['chain'].upper()}) LAUNCH STATUS - CONFIRMED*"
        was_will_be = "was"
        callback_data = (
            "launch_with_loan"
            if status_text["loan"]
            else "launch_without_loan"
        )

    team_tokens = int(status_text["supply"]) * (
        int(status_text["percent"]) / 100
    )
    liquidity_tokens = int(status_text["supply"]) - team_tokens

    if callback_data == "launch_with_loan":
        price_native = float(status_text["loan"]) / liquidity_tokens
        loan_info = (
            f"Loan Supply: {liquidity_tokens:,.0f}\n"
            f"Loan Amount: {status_text['loan']} {chain_info.native.upper()}\n"
            f"Loan Duration: {status_text['duration']} Days\n"
        )
        if status_text["complete"] == 1:
            loan_info += (
                f"Loan Due: {status_text['due']}\n"
                f"Loan ID: {status_text['loan_id']}\n"
            )
    else:
        price_native = (int(status_text["fee"]) / 10**18) / liquidity_tokens
        loan_info = ""

    price_usd = (
        price_native
        * await etherscan.get_native_price(status_text["chain"])
        * 2
    )
    market_cap_usd = price_usd * int(status_text["supply"]) * 2

    await update.message.reply_text(
        f"{header}\n\n"
        f"Ticker: {status_text['ticker']}\n"
        f"Name: {status_text['name']}\n"
        f"{token_text}"
        f"Taxes: {status_text['buy_tax']}/{status_text['sell_tax']}\n"
        f"Total Supply: {float(status_text['supply']):,.0f}\n"
        f"Team Supply: {team_tokens:,.0f} ({status_text['percent']}%)\n"
        f"{loan_info}"
        f"Cost: {chain_info.w3.from_wei(int(status_text['fee']), 'ether')} {chain_info.native.upper()}\n\n"
        f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
        f"Ownership {was_will_be} transferred to:\n`{status_text['owner']}`\n\n"
        f"{message}\n\n"
        f"Current Deployer Wallet Balance:\n"
        f"{float(balance_str):,.6f} {chain_info.native.upper()}\n\n",
        parse_mode="Markdown",
        reply_markup=button,
    )


async def stuck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = await db.search_entry(user_id)
        data = await onchain.cancel_tx(
            status_text["chain"],
            status_text["address"],
            status_text["secret_key"],
        )
        await update.message.reply_text(data)


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = await db.search_entry(user_id)
        if status_text:
            result = await onchain.transfer_balance(
                status_text["chain"],
                status_text["address"],
                status_text["owner"],
                status_text["secret_key"],
            )
            if result.startswith("Error"):
                await update.message.reply_text(
                    f"Error\n\n{result}\n\n"
                    "If this is unexpected use your saved private key from setup to withdraw funds",
                )
            else:
                chain_link = await chains.get_chain_info(
                    status_text["chain"]
                ).scan_tx
                await update.message.reply_text(
                    f"Balance withdrawn\n\n{chain_link}{result}\n\n"
                    "You can now safely use /reset to reset your project"
                )

        else:
            await update.message.reply_text(
                "No projects waiting, please use /launch to start"
            )


HANDLERS = [
    (func.__name__.split("_")[0], func, description)
    for func, description in [
        (id, "Your TG ID"),
        (launch, "launch your project"),
        (reset, "Reset your project"),
        (start, "About Xchange Create"),
        (status, "Your project status"),
        (stuck, "Clear a stuck txn"),
        (withdraw, "Withdraw funds"),
    ]
]
