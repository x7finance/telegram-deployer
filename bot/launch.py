from telegram import *
from telegram.ext import *

from eth_utils import is_checksum_address
from eth_account import Account
from datetime import datetime

from constants import ca, bot, chains
from hooks import api, db, deployments

chainscan = api.ChainScan()

STAGE_CHAIN, STAGE_TICKER, STAGE_NAME, STAGE_SUPPLY, STAGE_AMOUNT, STAGE_LOAN, STAGE_DURATION, STAGE_OWNER, STAGE_CONFIRM = range(9)

async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            await update.message.reply_text(
                f"Currently awaiting launch for {status_text['ticker']} ({status_text['chain']})\n\n"
                f"Fund `{status_text['address']}` with {int(status_text['fee']) / 10 ** 18} ETH + a little for gas\n\n"
                f"Ownership will be transferred to:\n{status_text['owner']}\n\n"
                f"To clear this deployment use /reset",
                parse_mode="Markdown"
            )
        else:
            buttons = [
                [InlineKeyboardButton(chain.upper(), callback_data=f'chain_{chain.lower()}')]
                for chain in chains.live
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                f"Lets get you launched by answering a few questions about your project...\n\n"
                f"First, select your chain:",
                reply_markup=keyboard
            )
            return STAGE_CHAIN

async def stage_chain(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chain = query.data.split('_')[1].upper()
    context.user_data['chain'] = chain
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"{context.user_data['chain']} Chain\n\nBrilliant! Now, what's the project's token ticker?"
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
    buttons = [
        [InlineKeyboardButton("0", callback_data=f'amount_0')],
        [InlineKeyboardButton("5%", callback_data=f'amount_5')],
        [InlineKeyboardButton("10%", callback_data=f'amount_10')],
        [InlineKeyboardButton("25%", callback_data=f'amount_25')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        f"{context.user_data['supply']} Total supply\n\nThanks! Now, What percentage of tokens do you want to keep back as 'team supply'?",
        reply_markup=keyboard
    )
    return STAGE_AMOUNT

async def stage_amount(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    amount = query.data.split('_')[1]
    context.user_data['amount'] = amount
    buttons = [
        [InlineKeyboardButton("1 ETH", callback_data=f'loan_1')],
        [InlineKeyboardButton("2 ETH", callback_data=f'loan_2')],
        [InlineKeyboardButton("3 ETH", callback_data=f'loan_3')],
        [InlineKeyboardButton("4 ETH", callback_data=f'loan_4')],
        [InlineKeyboardButton("5 ETH", callback_data=f'loan_5')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if amount == "0":
        amount_str = 'No tokens will be held, 100% of tokens will go into the liquidity.'
    else:
        amount_str = f"{amount}% of tokens will be held as team supply."
    pool = deployments.get_pool_funds("base-sepolia")
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"{amount_str}\n\nThanks! Now, how much ETH do you want in Initial Liquidity?\n\nCurrently Available: {pool / 10 ** 18} ETH\n",
        reply_markup=keyboard
    )
    return STAGE_LOAN

async def stage_loan(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    loan_amount = query.data.split('_')[1]
    context.user_data['loan'] = loan_amount
    buttons = [
        [InlineKeyboardButton("1 Day", callback_data=f'duration_1')],
        [InlineKeyboardButton("2 Days", callback_data=f'duration_2')],
        [InlineKeyboardButton("3 Days", callback_data=f'duration_3')],
        [InlineKeyboardButton("4 Days", callback_data=f'duration_4')],
        [InlineKeyboardButton("5 Days", callback_data=f'duration_5')],
        [InlineKeyboardButton("6 Days", callback_data=f'duration_5')],
        [InlineKeyboardButton("7 Days", callback_data=f'duration_5')]

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"{loan_amount} ETH will be allocated for initial liquidity.\n\nHow long do you want the loan for?",
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
        text=f"{duration} days, If the loan is not paid before then, the loan is eligible for liquidiation meaning the loaned amount will be withdrawn from the pair liquidity\n\n"
        "Now Please provide the address you want ownership transferred to."
    )
    return STAGE_OWNER


async def stage_owner(update: Update, context: CallbackContext) -> int:
    context.user_data['owner'] = update.message.text
    if not is_checksum_address(context.user_data['owner']):
        await update.message.reply_text("Error: Invalid Ethereum address. Please enter a valid checksum address.")
        return STAGE_OWNER
    else:
        user_data = context.user_data
        ticker = user_data.get('ticker')
        name = user_data.get('name')
        chain = user_data.get('chain')
        supply = user_data.get('supply')
        amount = user_data.get('amount')
        loan = user_data.get('loan')
        duration = user_data.get('duration')
        address = user_data.get('owner')

        if all([ticker, name, chain, supply, amount, loan, duration, address]):

            loan_in_wei = int(loan) * 10 ** 18
            origination_fee = loan_in_wei * 3 // 100
            loan_deposit = bot.LOAN_DEPOSIT * 10 ** 18
            fee = origination_fee + loan_deposit
            context.user_data['fee'] = fee

            team_tokens = int(supply) * (int(amount) / 100)
            liquidity_tokens = int(supply) - team_tokens

            price_eth = int(loan) / liquidity_tokens
            price_usd = price_eth * chainscan.get_native_price(chain.lower()) * 2
            market_cap_usd = price_usd * int(supply) * 2

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "Thank you, Please check the values below\n\n"
                    f"Chain: {chain}\n"
                    f"Ticker: {ticker}\n"
                    f"Project Name: {name}\n"
                    f"Total Supply: {supply}\n"
                    f"Team Supply: {amount}%\n"
                    f"Loan Amount: {loan} ETH\n"
                    f"Loan Duration: {duration} Days\n"
                    f"Cost: {int(fee) / 10 ** 18} ETH\n\n"
                    f"Ownership of the project will be transferred to:\n`{address}`\n\n"
                    f"Launch Token Price: ${price_usd:.8f}\n"
                    f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
                    "Do you want to proceed with the launch?"
                ),
                parse_mode="Markdown"
            )
            return STAGE_CONFIRM
        else:
            await update.message.reply_text("Error: Incomplete information provided.")
            return ConversationHandler.END


async def stage_confirm(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_response = update.message.text.lower()
    if user_response == "yes":
        user = update.effective_user
        user_name = user.username or f"{user.first_name} {user.last_name}"
        user_id = user.id
        account = Account.create()
        now = datetime.now()
        db.add_entry(now, 
                      user_name, 
                      user_id, 
                      account.address, 
                      account.key.hex(), 
                      user_data.get('chain'), 
                      user_data.get('ticker'),
                      user_data.get('name'), 
                      user_data.get('supply'), 
                      user_data.get('amount'), 
                      user_data.get('loan'),
                      user_data.get('duration'), 
                      user_data.get('owner'),
                      int(user_data.get('fee'))
                      )
        await update.message.reply_text(f'Please send {int(user_data.get('fee')) / 10 ** 18} ETH to the following address:\n\n`{account.address}`.\n\n'
                                        '*Make a note of this wallet address as your reference number*\n\n'
                                        'To check the status of your launch use /status',
                parse_mode="Markdown")
        return ConversationHandler.END

    elif user_response == "no":
        await update.message.reply_text("Project cancelled. You can start over with /launch.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please reply with 'yes' or 'no'.")
        return STAGE_CONFIRM


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("launch canceled.")
    return ConversationHandler.END


async def function(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    status_text = db.search_entry_by_user_id(user_id)
    
    if not status_text:
        await query.edit_message_text("No deployment status found")
        return
    
    chain_url = chains.chains[status_text["chain"].lower()].scan_token
    token_0 = chains.chains[status_text["chain"].lower()].address
    chain_id = chains.chains[status_text["chain"].lower()].id

    team_supply = int(status_text["supply"]) * int(status_text["amount"])
    loan_supply = int(status_text["supply"]) - team_supply

    try:
        await query.edit_message_text(
            f"Deploying {status_text['ticker']} ({status_text['chain']})...."
        )
        result = deployments.deploy_token(
            status_text["chain"].lower(),
            status_text["name"],
            status_text["ticker"],
            status_text["supply"],
            loan_supply,
            int(status_text["loan"]) * 10 ** 18,
            int(status_text["duration"]) * 60 * 60 * 24,
            status_text["owner"],
            status_text["address"],
            status_text["secret_key"],
            status_text["fee"]
        )
        
        if isinstance(result, str) and result.startswith("Error"):
            await query.edit_message_text(f"{result}\n\nIf you want to cancel the deployment and get your funds back use /withdraw")
            return
        
        token_address, pair_address = result
        
        refund = deployments.transfer_balance(
            status_text["chain"].lower(),
            status_text["address"],
            status_text["owner"],
            status_text["secret_key"]
        )
        
        if isinstance(refund, str) and refund.startswith("Error"):
            await query.edit_message_text(refund)
            return
        
        await query.edit_message_text(
            f"Congrats {status_text['ticker']} has been launched and an Xchange ILL Created\n\n"
            f"CA: `{token_address}`\n\n"
            f"Ownership transferred to:\n"
            f"`{status_text['owner']}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="Token Contract", url=f"{chain_url}{token_address}")],
                    [InlineKeyboardButton(text="Pair Contract", url=f"{chain_url}{pair_address}")],
                    [InlineKeyboardButton(text="Buy Link", url=f"x7finance.org//swap?chainId={chain_id}&token0={token_0}&token1={token_address}")],
                    [InlineKeyboardButton(text="Loan Dashboard", url=f"https://www.x7finance.org/loans?tab=open-positions")]
                ]
            )
        )
        
        db.set_complete(status_text["address"])
    
    except Exception as e:
        await query.edit_message_text(f"Error deploying token: {str(e)}\n\nIf you want to cancel the deployment and get your funds back use /withdraw")
