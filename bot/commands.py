from telegram import *
from telegram.ext import *
from web3 import Web3

from constants import chains, bot
from hooks import api, db, functions, tools

chainscan = api.ChainScan()

async def test(update: Update, context: CallbackContext) -> int:
    return


async def id(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        await update.message.reply_text(
            f"{update.effective_user.username}, Your user ID is: `{update.effective_user.id}`",
        parse_mode="Markdown"
    )


async def reset(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry(user_id)
        
        if not status_text:
            await update.message.reply_text(
                "No projects waiting, please use /launch to start"
            )
            return
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='reset_yes'),
            InlineKeyboardButton("No", callback_data='reset_no')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Are you sure you want to reset your project?\n\nPlease ensure you have no remaining "
        "funds in the designated deployer address or you have saved the address and private "
        "key\n\n*This action cannot be undone*",
    parse_mode="Markdown",
    reply_markup=reply_markup
    )


async def reset_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == 'reset_yes':
        delete_text = db.delete_entry(user_id)
        if delete_text:
            await query.edit_message_text(
                "Project reset. Use /launch to start a new project"
            )
        else:
            await query.edit_message_text(
                "No projects waiting, please use /launch to start"
            )
    elif query.data == 'reset_no':
        await query.edit_message_text("Reset canceled.")


async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    user_name = user.username or f"{user.first_name} {user.last_name}"
    chat_type = update.message.chat.type
    count = db.count_launches()
    _, loan_fees = tools.generate_loan_terms("base", 1)
    if chat_type == "private":
        await update.message.reply_text(
            f"Welcome to {tools.escape_markdown(bot.BOT_NAME)}, {tools.escape_markdown(user_name)}!\n"
            f"Your gateway to creating and launching tokens in just minutes.\n\n"
            f"*Here's what you can do:*\n"
            "- Launch a Token: Seamlessly create and deploy your token.\n"
            f"- Borrow Liquidity: {loan_fees}\n\n"
            "*Key Features:*\n"
            "- Flexible Loan Terms: Choose your preferred loan duration. If unpaid by the expiry date, "
            "repayment will occur through pair liquidity.\n"
            f"- Refundable Deposit: The {bot.LIQUIDATION_DEPOSIT} ETH liquidation deposit is fully "
            "returned once your loan is settled.\n\n"
            f"Join the innovators—{count} tokens launched and counting!\n\n"
            "*Ready to launch your project?\n*"
            "use /launch to start your project now!",
        parse_mode="Markdown"
        )


async def status(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry(user_id)
        
        if status_text:
            chain_web3 = chains.chains[status_text["chain"]].w3
            chain_native = chains.chains[status_text["chain"]].token
            web3 = Web3(Web3.HTTPProvider(chain_web3))
            balance_wei = web3.eth.get_balance(status_text["address"])
            balance = web3.from_wei(balance_wei, 'ether')
            balance_str = format(balance, '.18f')

            if status_text["loan"] == "0":
                loan_deployment = False
                gas_estimate = functions.estimate_gas_without_loan(
                    status_text["chain"],
                    status_text["name"],
                    status_text["ticker"],
                    int(status_text["supply"]),
                    int(status_text["percent"]),
                    status_text["description"], 
                    status_text["twitter"], 
                    status_text["telegram"],
                    status_text["website"],
                    status_text["owner"],
                    int(status_text["fee"])
                    )

            else:
                loan_deployment = True
                gas_estimate = functions.estimate_gas_with_loan(
                    status_text["chain"],
                    status_text["name"],
                    status_text["ticker"],
                    int(status_text["supply"]),
                    int(status_text["percent"]),
                    status_text["description"], 
                    status_text["twitter"], 
                    status_text["telegram"],
                    status_text["website"],
                    web3.to_wei(status_text["loan"], 'ether'),
                    int(status_text["duration"]) * 60 * 60 * 24,
                    status_text["owner"],
                    int(status_text["fee"])
                    )

            if status_text["complete"] == 0:
                total_cost = int(status_text["fee"]) + gas_estimate
                if balance_wei >= total_cost:
                    if loan_deployment:
                        callback_data = "launch_with_loan"
                    else:
                        callback_data = "launch_without_loan"

                    button = InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(text="LAUNCH", callback_data=callback_data)],
                        ]
                    )
                    message = "Ready to launch, hit the button below!"
                    header = "*LAUNCH STATUS - READY*"
                    was_will_be = "will be"
                else:


                    message = (
                        f"Send `{status_text['address']}` with {round(web3.from_wei(total_cost, "ether"), 4)} {chain_native.upper()} (This includes gas fees)\n\n"
                        "Any fees not used will be returned to the wallet you designated as owner at deployment.\n\n"
                        "use /withdraw to return any un-used funds\n"
                        "use /reset to clear this launch"
                    )
                    header = "*LAUNCH STATUS - WAITING*"
                    was_will_be = "will be"
                    button = ""
            else:
                button = ""
                message = "use /withdraw to return any un-used funds\nuse /reset to clear this launch"
                header = "*LAUNCH STATUS - CONFIRMED*"
                was_will_be = "was"
            
            team_tokens = int(status_text["supply"]) * (int(status_text["percent"]) / 100)
            liquidity_tokens = int(status_text["supply"]) - team_tokens
            if loan_deployment:
                price_native = float(status_text["loan"]) / liquidity_tokens
                price_usd = price_native * chainscan.get_native_price(status_text["chain"]) * 2
                market_cap_usd = price_usd * int(status_text["supply"]) * 2

                supply_float = float(status_text["supply"])
                amount_percentage = float(status_text["percent"]) / 100
                team_supply = supply_float * amount_percentage
                loan_supply = supply_float - team_supply
                loan_info = (
                    f"Loan Supply: {loan_supply:,.0f}\n"
                    f"Loan Amount: {status_text['loan']} {chain_native.upper()}\n"
                    f"Loan Duration: {status_text['duration']} Days\n"
                )
            else:
                price_native = (int(status_text["fee"]) / 10 ** 18) / liquidity_tokens
                price_usd = price_native * chainscan.get_native_price(status_text["chain"]) * 2
                market_cap_usd = price_usd * int(status_text["supply"]) * 2
                loan_info = "No Loan, self-funded deployment.\n"
            await update.message.reply_text(
                f"{header}\n\n"
                f"{status_text['ticker']} ({status_text['chain'].upper()})\n\n"
                f"Project Name: {status_text['name']}\n"
                f"Desciption: {status_text['description']}\n"
                f"Twitter: {status_text['twitter']}\n"
                f"Telegram: {status_text['telegram']}\n"
                f"Website: {status_text['website']}\n"
                f"Total Supply: {float(status_text['supply']):,.0f}\n"
                f"Team Supply: {team_tokens:,.0f} ({status_text['percent']}%)\n"
                f"{loan_info}"
                f"Cost: {web3.from_wei(int(status_text['fee']), 'ether')} {chain_native.upper()}\n\n"
                f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
                f"Ownership {was_will_be} transferred to:\n`{status_text['owner']}`\n\n"
                f"{message}\n\n"
                f"Current Deployer Wallet Balance:\n"
                f"{float(balance_str):,.6f} {chain_native.upper()}\n\n",
            parse_mode="Markdown",
            reply_markup=button
            )
        else:
            await update.message.reply_text("No projects waiting, please use /launch to start")


async def withdraw(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry(user_id)
        if status_text:
            result = functions.transfer_balance(
                status_text["chain"],
                status_text["address"],
                status_text["owner"],
                status_text["secret_key"]
                )
            if result.startswith("Error"):
                await update.message.reply_text(
                    f"Error\n\n{result}\n\n"
                    "If this is unexpected use your saved private key from setup to withdraw funds",
        )
            else:
                chain_link = chains.chains[status_text["chain"]].scan_tx
                await update.message.reply_text(
                    f"Balance withdrawn\n\n{chain_link}{result}\n\n"
                    "You can now safely use /reset to reset your project")

        else:
            await update.message.reply_text("No projects waiting, please use /launch to start")




