from telegram import *
from telegram.ext import *

from eth_utils import is_checksum_address
from eth_account import Account
from datetime import datetime
from web3 import Web3
from decimal import Decimal

from constants import bot, chains, urls
from hooks import api, db, deployments

chainscan = api.ChainScan()

STAGE_CHAIN, STAGE_TICKER, STAGE_NAME, STAGE_SUPPLY, STAGE_AMOUNT, STAGE_LOAN, STAGE_DURATION, STAGE_OWNER, STAGE_CONFIRM = range(9)

async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            chain_web3 = chains.chains[status_text["chain"]].w3
            chain_native = chains.chains[status_text["chain"]].token
            web3 = Web3(Web3.HTTPProvider(chain_web3))
            balance_wei = web3.eth.get_balance(status_text["address"])
            balance = web3.from_wei(balance_wei, 'ether')
            balance_str = format(balance, '.18f')
            if status_text["complete"] == 0:
                if balance_wei >= int(status_text["fee"]):
                    button = InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(text="LAUNCH", callback_data="launch")],
                            ]
                        )
                    message = "Ready to launch, hit the button below!"
                    header = "*LAUNCH STATUS - READY*"
                    was_will_be = "will be"
                else:
                    message = (
                        f"Fund `{status_text["address"]}` with {web3.from_wei(int(status_text["fee"]), 'ether')} {chain_native.upper()} + a little for gas.\n\n"
                        "Any fees not used will be returned to your account at deployment.\n\n"
                        "use /withdraw to retrieve any funds\n"
                        "use /reset to clear this launch"
                        )
                    header = "*LAUNCH STATUS - WAITING*"
                    was_will_be = "will be"
                    button = ""
            else:
                button = ""
                message = "use /withdraw to retrieve any funds\nuse /reset to clear this launch"
                header = "*LAUNCH STATUS - CONFIRMED*"
                was_will_be = "was"

            team_tokens = int(status_text["supply"]) * (int(status_text["percent"]) / 100)
            liquidity_tokens = int(status_text["supply"]) - team_tokens

            price_eth = float(status_text["loan"]) / liquidity_tokens
            price_usd = price_eth * chainscan.get_native_price(status_text["chain"]) * 2
            market_cap_usd = price_usd * int(status_text["supply"]) * 2

            supply_float = float(status_text["supply"])
            amount_percentage = float(status_text["percent"]) / 100
            team_supply = supply_float * amount_percentage
            loan_supply = supply_float - team_supply

            await update.message.reply_text(
                f"{header}\n\n"
                f"{status_text["ticker"]} ({status_text["chain"]})\n\n"
                f"Project Name: {status_text["name"]}\n"
                f"Total Supply: {supply_float:,.0f}\n"
                f"Team Supply: {team_supply:,.0f} ({status_text["percent"]}%)\n"
                f"Loan Supply: {loan_supply:,.0f}\n"
                f"Loan Amount: {status_text["loan"]} {chain_native.upper()}\n"
                f"Loan Duration {status_text["duration"]} Days\n"
                f"Cost: {web3.from_wei(int(status_text["fee"]), 'ether')} {chain_native.upper()}\n\n"
                f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
                f"Ownership {was_will_be} transfered to:\n`{status_text["owner"]}`\n\n"
                f"Current Deployer Wallet Balance:\n"
                f"{balance_str} {chain_native.upper()}\n\n"
                f"{message}",
            parse_mode="Markdown",
            reply_markup=button
            )
        else:
            buttons = [
                [InlineKeyboardButton(chain.upper(), callback_data=f'chain_{chain.lower()}')]
                for chain in chains.live
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                f"Let's get you launched by answering a few questions about your project...\n\n"
                f"use /cancel at any time to end the conversation.\n\n"
                f"First, select your chain:",
                reply_markup=keyboard
            )
            return STAGE_CHAIN

async def stage_chain(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chain = query.data.split('_')[1].lower()
    context.user_data['chain'] = chain
    chain_native = chains.chains[chain.lower()].token
    funds = deployments.get_pool_funds(chain.lower())
    if funds < bot.MIN_LOAN_AMOUNT:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=
                f"There's currently only {funds} {chain_native.upper()} in the {context.user_data['chain']} Chain lending pool.\n\n"
                f"Pop back later once the pool is refilled, or check the link below to see how you can deposit your {chain_native.upper()} and earn yield!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("X7D Lending Dashboard", url=urls.XCHANGE_FUND)]
            ])
        )
        return ConversationHandler.END
    else:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=
                f"{context.user_data['chain'].upper()} Chain Selected.\n\nBrilliant!\n\n"
                f"There's currently {funds} {chain_native.upper()} in the lending pool ready to be deployed, so let's get your project launched!\n\n"
                "Now, what's the project's token ticker?"
            )
        return STAGE_TICKER

async def stage_ticker(update: Update, context: CallbackContext) -> int:
    context.user_data['ticker'] = update.message.text
    if len(context.user_data['ticker']) > 5:
        await update.message.reply_text(
            "Error: The ticker must be 5 characters or fewer. Please enter a valid ticker."
        )
        return STAGE_TICKER 
    await update.message.reply_text(
        f"{context.user_data['ticker']}\n\nGreat! Now, please reply with your project name."
    )
    return STAGE_NAME

async def stage_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        f"{context.user_data['name']}\n\nGot it! Now, what do you want the total supply of your token to be?"
    )
    return STAGE_SUPPLY

async def stage_supply(update: Update, context: CallbackContext) -> int:
    supply_input = update.message.text.strip()
    if not (supply_input.isdigit() and int(supply_input) > 0):
        await update.message.reply_text(
            "Error: Total supply should be a whole number greater than zero, with no decimals. Please try again."
        )
        return STAGE_SUPPLY
    context.user_data['supply'] = supply_input
    supply_float = float(supply_input)
    buttons = [
        [InlineKeyboardButton("0%", callback_data=f'amount_0')]
#        ,
#        [InlineKeyboardButton("5%", callback_data=f'amount_5')],
#        [InlineKeyboardButton("10%", callback_data=f'amount_10')],
#        [InlineKeyboardButton("25%", callback_data=f'amount_25')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        f"{supply_float:,.0f} Total Supply.\n\nThanks! Now, what percentage of tokens (if any) do you want to keep back as 'team supply'?\n\n"
        "These tokens will not be added to initial liquidity.",
        reply_markup=keyboard
    )
    return STAGE_AMOUNT

async def stage_amount(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    percent = query.data.split('_')[1]
    chain_native = chains.chains[context.user_data['chain']].token
    context.user_data['percent'] = percent
    buttons = [
        [InlineKeyboardButton(f"0.5 {chain_native.upper()}", callback_data=f'loan_0.5')],
#        [InlineKeyboardButton(f"1 {chain_native.upper()}", callback_data=f'loan_1')],
#        [InlineKeyboardButton(f"2 {chain_native.upper()}", callback_data=f'loan_2')],
#        [InlineKeyboardButton(f"3 {chain_native.upper()}", callback_data=f'loan_3')],
#        [InlineKeyboardButton(f"4 {chain_native.upper()}", callback_data=f'loan_4')],
#        [InlineKeyboardButton(f"5 {chain_native.upper()}", callback_data=f'loan_5')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if percent == "0":
        percent_str = 'No tokens will be held, and 100% of tokens will go into the liquidity.'
    else:
        percent_str = f"{percent}% of tokens will be held as team supply."
    pool = deployments.get_pool_funds(context.user_data['chain'])
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"{percent_str}\n\nThanks! Now, how much {chain_native.upper()} do you want in initial liquidity?\n\n"
        f"Currently Available: {pool} {chain_native.upper()}\n",
        reply_markup=keyboard
    )
    return STAGE_LOAN

async def stage_loan(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    loan_amount = query.data.split('_')[1]
    pool = deployments.get_pool_funds(context.user_data['chain'])
    if Decimal(loan_amount) > pool:
        chain_native = chains.chains[context.user_data['chain']].token
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Error: There is only {pool} {chain_native} available. Please try again."
            )
        return STAGE_LOAN
    chain_native = chains.chains[context.user_data['chain']].token
    context.user_data['loan'] = loan_amount
    buttons = [
#       [InlineKeyboardButton("1 Day", callback_data=f'duration_1')],
#        [InlineKeyboardButton("2 Days", callback_data=f'duration_2')],
#        [InlineKeyboardButton("3 Days", callback_data=f'duration_3')],
#        [InlineKeyboardButton("4 Days", callback_data=f'duration_4')],
#        [InlineKeyboardButton("5 Days", callback_data=f'duration_5')],
#        [InlineKeyboardButton("6 Days", callback_data=f'duration_6')],
        [InlineKeyboardButton("7 Days", callback_data=f'duration_7')]

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"{loan_amount} {chain_native.upper()} will be allocated for initial liquidity.\n\n"
            "How long do you want the loan for?",
        reply_markup=keyboard
    )
    return STAGE_DURATION

async def stage_duration(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    duration = query.data.split('_')[1]
    context.user_data['duration'] = duration
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"Loan duration will be {duration} days.\n\n"
        "If the loan is not fully paid before then, it will become eligible for liquidation. This means the loan amount can be withdrawn from the pair liquidity, potentially resulting in a decrease to the token value.\n\n"
        "Now, please provide the address you want ownership transferred to."
    )
    return STAGE_OWNER


async def stage_owner(update: Update, context: CallbackContext) -> int:
    context.user_data['owner'] = update.message.text
    if not is_checksum_address(context.user_data['owner']):
        await update.message.reply_text("Error: Invalid address. Please enter a valid checksum address.")
        return STAGE_OWNER
    
    user_data = context.user_data
    ticker = user_data.get('ticker')
    name = user_data.get('name')
    chain = user_data.get('chain')
    supply = user_data.get('supply')
    percent = user_data.get('percent')
    loan = user_data.get('loan')
    duration = user_data.get('duration')
    address = user_data.get('owner')

    if all([ticker, name, chain, supply, percent, loan, duration, address]):

        chain_web3 = chains.chains[chain].w3
        web3 = Web3(Web3.HTTPProvider(chain_web3))

        fee, _, _ = bot.ACTIVE_LOAN(chain, loan)
        context.user_data['fee'] = fee

        team_tokens = int(supply) * (int(percent) / 100)
        liquidity_tokens = int(supply) - team_tokens

        price_eth = float(loan) / liquidity_tokens
        price_usd = price_eth * chainscan.get_native_price(chain.lower()) * 2
        market_cap_usd = price_usd * int(supply) * 2

        supply_float = float(supply)
        amount_percentage = float(percent) / 100
        team_supply = supply_float * amount_percentage
        loan_supply = supply_float - team_supply

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="confirm_yes")],
            [InlineKeyboardButton("No", callback_data="confirm_no")]
        ])

        await update.message.reply_text(
            f"Thank you! Please check the values below:\n\n"
            f"Chain: {chain}\n"
            f"Ticker: {ticker}\n"
            f"Project Name: {name}\n"
            f"Total Supply: {supply_float:,.0f}\n"
            f"Team Supply: {team_supply:,.0f} ({percent}%)\n"
            f"Loan Supply: {loan_supply:,.0f}\n"
            f"Loan Amount: {loan} ETH\n"
            f"Loan Duration: {duration} Days\n"
            f"Cost: {web3.from_wei(fee, 'ether')} ETH\n\n"
            f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
            f"Ownership of the project will be transferred to:\n`{address}`\n\n"
            "Do you want to proceed with the launch?",
            parse_mode="Markdown",
            reply_markup=buttons
        )
        
        return STAGE_CONFIRM
    else:
        await update.message.reply_text("Error: Incomplete information provided.")
        return ConversationHandler.END


async def stage_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_data = context.user_data
    confirm = query.data.split('_')[1]
    
    if confirm == "yes":
        user = update.effective_user
        user_name = user.username or f"{user.first_name} {user.last_name}"
        user_id = user.id
        account = Account.create()
        now = datetime.now()
        db.add_entry(
            now, 
            user_name, 
            user_id, 
            account.address, 
            account.key.hex(), 
            user_data.get('chain'), 
            user_data.get('ticker'),
            user_data.get('name'), 
            user_data.get('supply'), 
            user_data.get('percent'), 
            user_data.get('loan'),
            user_data.get('duration'), 
            user_data.get('owner'),
            int(user_data.get('fee'))
        )

        chain_web3 = chains.chains[user_data.get('chain')].w3
        web3 = Web3(Web3.HTTPProvider(chain_web3))

        chain_native = chains.chains[user_data.get('chain')].token

        await query.message.reply_text(
            
            f"Please send {web3.from_wei(user_data.get('fee'), 'ether')} {chain_native} + a little for gas to the following address:\n\n"
            f"`{account.address}`\n\n"
            "Any fees not used will be returned to your account at deployment.\n\n"
            "*Make a note of this wallet address as your reference number.*\n\n"
            "To check the status of your launch use /status",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    elif confirm == "no":
        await query.message.reply_text("Project canceled. You can start over with /launch.")
        return ConversationHandler.END



async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Launch canceled.")
    return ConversationHandler.END


async def function(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    status_text = db.search_entry_by_user_id(user_id)
    
    if not status_text:
        await query.edit_message_text("No deployment status found")
        return
    chain = status_text["chain"]
    chain_url = chains.chains[chain].scan_token
    token_0 = chains.chains[chain].address
    chain_id = chains.chains[chain].id
    chain_scan = chains.chains[chain].scan_address
    chain_tx = chains.chains[chain].scan_tx
    chain_dext = chains.chains[chain].dext
    _, loan_contract, _ = bot.ACTIVE_LOAN(chain, status_text["loan"])

    chain_web3 = chains.chains[chain].w3
    web3 = Web3(Web3.HTTPProvider(chain_web3))

    await query.edit_message_text(
        f"Deploying {status_text['ticker']} ({status_text['chain']})...."
    )

    loan = deployments.deploy_token(
        status_text["chain"],
        status_text["name"],
        status_text["ticker"],
        int(status_text["supply"]),
        int(status_text["percent"]),
        web3.to_wei(status_text["loan"], 'ether'),
        int(status_text["duration"]) * 60 * 60 * 24,
        status_text["owner"],
        status_text["address"],
        status_text["secret_key"],
        int(status_text["fee"])
    )
    
    if isinstance(loan, str) and loan.startswith("Error"):
        await query.edit_message_text(f"Error initiating TX.\n\nIf you want to cancel the deployment and get your funds back use /withdraw")
        print(loan)
        return
    
    token_address, pair_address, loan_id = loan
    
    refund = deployments.transfer_balance(
        status_text["chain"],
        status_text["address"],
        status_text["owner"],
        status_text["secret_key"]
    )
    
    if isinstance(refund, str) and refund.startswith("Error"):
        refund_text = f"Error retrieving funds\n\nUse /withdraw to claim any unused funds"
        print(refund)
    else:
        refund_text = (
            "Excess funds withdrawn\n\n"
            f"{chain_tx}{refund}"
        )

    try:
        contract = web3.eth.contract(address=web3.to_checksum_address(loan_contract), 
                                     abi=chainscan.get_abi(loan_contract, chain))
        schedule1 = contract.functions.getPremiumPaymentSchedule(int(loan_id)).call()
        schedule2 = contract.functions.getPrincipalPaymentSchedule(int(loan_id)).call()
        schedule = api.format_schedule(schedule1, schedule2, "ETH")
    except Exception:
        schedule = "Unavailable"
    
    await query.edit_message_text(
        f"Congrats {status_text['ticker']} has been launched and an Xchange ILL Created\n\n"
        f"CA: `{token_address}`\n\n"
        f"Loan ID: {loan_id}\n\n"
        f"Ownership transferred to:\n"
        f"`{status_text['owner']}`\n\n"
        f"Payment Schedule:\n\n"
        f"{schedule}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Token Contract", url=f"{chain_url}{token_address}")],
                [InlineKeyboardButton(text="Pair Contract", url=f"{chain_url}{pair_address}")],
                [InlineKeyboardButton(text="Buy Link", url=f"{urls.XCHANGE_BUY(chain_id, token_address)}")],
                [InlineKeyboardButton(text="Chart", url=f"{urls.DEX_TOOLS(chain_dext)}{token_address}")],
                [InlineKeyboardButton(text="Loan Dashboard", url=urls.XCHANGE_LOANS)],
                [InlineKeyboardButton(text="Loan Contract", url=f"{chain_scan}{loan_contract}#writeContract#F7")]
            ]
        )
    )
    
    db.set_complete(status_text["address"])
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=refund_text
    )
