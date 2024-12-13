from telegram import *
from telegram.ext import *

from eth_utils import is_checksum_address
from eth_account import Account
from datetime import datetime
from decimal import Decimal, InvalidOperation

from constants import ca, bot, chains, urls
from hooks import api, db, functions, tools

chainscan = api.ChainScan()

STAGE_CHAIN, STAGE_TICKER, STAGE_NAME, STAGE_SUPPLY, STAGE_AMOUNT, STAGE_DESCRIPTION, STAGE_TWITTER, STAGE_TELEGRAM, STAGE_WEBSITE, STAGE_BUY_TAX, STAGE_SELL_TAX, STAGE_LOAN, STAGE_DURATION, STAGE_OWNER, STAGE_CONFIRM, STAGE_CONTRIBUTE = range(16)


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry(user_id)
        
        if status_text:
            await update.message.reply_text(
                f"You already have a token launch pending, use /status to see it",
            parse_mode="Markdown"
            )
        else:
            buttons = [
                [InlineKeyboardButton(chain.upper(), callback_data=f'chain_{chain.lower()}')]
                for chain in chains.live
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                f"Let's get your project launched by answering a few questions...\n\n"
                f"use /cancel at any time to end the conversation\n\n"
                f"First, select your chain:",
                reply_markup=keyboard
            )
            return STAGE_CHAIN


async def stage_chain(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chain = query.data.split('_')[1].lower()
    context.user_data['chain'] = chain
    chain_native = chains.chains[chain.lower()].native
    funds = functions.get_pool_funds(chain.lower())
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=
            f"{context.user_data['chain'].upper()} Chain Selected.\n\n"
            f"There's currently {funds} {chain_native.upper()} in the lending pool ready to be deployed, so let's get your project launched!\n\n"
            "What's the project's token ticker?"
        )
    return STAGE_TICKER


async def stage_ticker(update: Update, context: CallbackContext) -> int:
    if len(update.message.text) > 6 or tools.detect_emojis(update.message.text):
        await update.message.reply_text(
            "Error: The ticker must be 6 standard characters or fewer. Please enter a valid ticker"
        )
        return STAGE_TICKER 
    
    context.user_data['ticker'] = update.message.text
    await update.message.reply_text(
        f"Ticker: {context.user_data['ticker']}\n\nWhat is your project's name"
    )
    return STAGE_NAME


async def stage_name(update: Update, context: CallbackContext) -> int:
    if len(update.message.text) > 30 or tools.detect_emojis(update.message.text):
        await update.message.reply_text(
            "Error: The name must be 30 standard characters or fewer. Please enter a valid name"
        )
        return STAGE_NAME

    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        f"Name: {context.user_data['name']}\n\nPlease write a short description of your project (in 200 characters or less)"
    )
    return STAGE_DESCRIPTION


async def stage_description(update: Update, context: CallbackContext) -> int:
    if len(update.message.text) > 200:
        await update.message.reply_text(
            "Error: The description must be 200 characters or fewer. Please try again"
        )
        return STAGE_DESCRIPTION 
    
    context.user_data['description'] = update.message.text
    await update.message.reply_text(
        f"Recieved!\n\nNow, if you have one please provide the twitter link or type 'None'"
    )
    return STAGE_TWITTER


async def stage_twitter(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()
    if user_input.lower() == "none":
        context.user_data['twitter'] = ""
        await update.message.reply_text(
            "No Twitter link.\n\nThank you! Now Please provide a Telegram Link, or 'none'."
        )
        return STAGE_TELEGRAM
    
    if not user_input.lower().startswith(("http://", "https://")):
        await update.message.reply_text(
            "Error: The Twitter link must start with http:// or https://, or type 'None' if not applicable. Please try again."
        )
        return STAGE_TWITTER
    
    context.user_data['twitter'] = user_input
    await update.message.reply_text(
        f"{context.user_data['twitter']}\n\nThank you! Now Please provide a Telegram Link, or 'none'."
    )
    return STAGE_TELEGRAM


async def stage_telegram(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()
    if user_input.lower() == "none":
        context.user_data['telegram'] = ""
        await update.message.reply_text(
            "Telegram link set as empty.\n\nNow, please provide the website link starting with http:// or https:// or type 'None' if not applicable."
        )
        return STAGE_WEBSITE
    
    if not user_input.lower().startswith(("http://", "https://")):
        await update.message.reply_text(
            "Error: The Telegram link must start with http:// or https://, or type 'None' if not applicable. Please try again."
        )
        return STAGE_TELEGRAM
    
    context.user_data['telegram'] = user_input
    await update.message.reply_text(
        f"{context.user_data['telegram']}\n\nNow, please provide the Website link starting with http:// or https:// or type 'None' if not applicable."
    )
    return STAGE_WEBSITE


async def stage_website(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()
    if user_input.lower() == "none":
        context.user_data['website'] = ""
        await update.message.reply_text(
            "Website link set as empty.\n\n"
            "What do you want the buy tax of your token to be? Between 0-20\n\n"
            "This can be changed after launch\n\n"
            "Tax wallet will be set as the wallet you designate as owner\n\n"
            "This can be a changed after launch"
        )
        return STAGE_BUY_TAX
    
    if not user_input.lower().startswith(("http://", "https://")):
        await update.message.reply_text(
            "Error: The Website link must start with http:// or https://, or type 'None' if not applicable. Please try again."
        )
        return STAGE_WEBSITE
    
    context.user_data['website'] = user_input
    await update.message.reply_text(
        f"{context.user_data['website']}\n\n"
        "What do you want the buy tax of your token to be? Between 0-20\n\n"
        "Tax wallet will be set as the wallet you designate as owner\n\n"
        "These can be a changed after launch"
    )
    return STAGE_BUY_TAX


async def stage_buy_tax(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()

    if user_input.isdigit():
        buy_tax = int(user_input)

        if 0 <= buy_tax <= 20:
            context.user_data['buy_tax'] = buy_tax
            await update.message.reply_text(
                f"Buy Tax will initially be set at {buy_tax}\n\n"
                "What do you want the sell tax to be? (0-20)"
            )
            return STAGE_SELL_TAX
        else:
            await update.message.reply_text(
                "Error: Tax should be a number between 0 and 20 (inclusive)."
            )
            return STAGE_BUY_TAX
    else:
        await update.message.reply_text(
            "Error: Please enter a valid number between 0 and 20."
        )
        return STAGE_BUY_TAX


async def stage_sell_tax(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()

    if user_input.isdigit():
        sell_tax = int(user_input)

        if 0 <= sell_tax <= 20:
            context.user_data['sell_tax'] = sell_tax
            await update.message.reply_text(
                f"Buy Tax will initially be set at {sell_tax}\n\n"
                "What do you want the total supply of your token to be?"
            )
            return STAGE_SUPPLY
        else:
            await update.message.reply_text(
                "Error: Tax should be a number between 0 and 20 (inclusive)."
            )
            return STAGE_SELL_TAX
    else:
        await update.message.reply_text(
            "Error: Please enter a valid number between 0 and 20."
        )
        return STAGE_SELL_TAX



async def stage_supply(update: Update, context: CallbackContext) -> int:
    supply_input = update.message.text.strip()
    if not (supply_input.isdigit() and int(supply_input) > 0):
        await update.message.reply_text(
            "Error: Total supply should be a whole number greater than zero, with no decimals. Please try again"
        )
        return STAGE_SUPPLY
    
    context.user_data['supply'] = supply_input
    supply_float = float(supply_input)
    buttons = [
        [InlineKeyboardButton("0%", callback_data=f'amount_0')],
        [InlineKeyboardButton("5%", callback_data=f'amount_5')],
        [InlineKeyboardButton("10%", callback_data=f'amount_10')],
        [InlineKeyboardButton("25%", callback_data=f'amount_25')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        f"{supply_float:,.0f} Total Supply\n\nWhat percentage of tokens (if any) do you want to keep back from the LP?\n\n"
        "These tokens will not be added to initial liquidity",
        reply_markup=keyboard
    )
    return STAGE_AMOUNT


async def stage_amount(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    percent = query.data.split('_')[1]
    chain = context.user_data['chain'].lower()
    chain_native = chains.chains[chain].native
    context.user_data['percent'] = percent
    pool = functions.get_pool_funds(chain)

    if percent == "0":
        percent_str = "No tokens will be held, and 100% of tokens will go into the liquidity"
    else:
        percent_str = f"{percent}% of tokens will be held as team supply"
    
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=(
            f"{percent_str}\n\n"
            f"How much {chain_native.upper()} (if any) do you want to borrow in initial liquidity?\n\n"
            f"Currently available to borrow: {pool} {chain_native.upper()}.\n\n"
            f"You can launch without a loan and supply the {chain_native.upper()} yourself by typing 0\n\n"
            "Please enter the amount as a number (e.g., 0, 1, 2.5):"
        )
    )
    return STAGE_LOAN


async def stage_loan(update: Update, context: CallbackContext) -> int:
    loan_input = update.message.text.strip()
    chain = context.user_data['chain'].lower()
    chain_native = chains.chains[chain].native
    pool = functions.get_pool_funds(chain)

    try:
        loan_amount = Decimal(loan_input)
    except InvalidOperation:
        await update.message.reply_text(
            f"Error: Please enter a valid number for the loan amount in {chain_native.upper()}. Try again."
        )
        return STAGE_LOAN

    if loan_amount < 0 or loan_amount > pool:
        await update.message.reply_text(
            f"Error: Loan amount must be between 0 and {pool} {chain_native.upper()}. Please try again."
        )
        return STAGE_LOAN

    if loan_amount > bot.MAX_LOAN_AMOUNT:
        await update.message.reply_text(
            f"Error: Maximum loan amount is {bot.MAX_LOAN_AMOUNT} {chain_native.upper()}. "
            f"Please enter an amount less than or equal to {bot.MAX_LOAN_AMOUNT}."
        )
        return STAGE_LOAN 

    if loan_amount == 0:
        await update.message.reply_text(
            text=f"No Loan. You'll front the liquidity yourself.\n\n"
                 f"Please enter the amount of {chain_native.upper()} you want to contribute to liquidity:"
        )
        return STAGE_CONTRIBUTE
    
    context.user_data['loan'] = float(loan_amount)

    await update.message.reply_text(
        text=(
            f"{loan_amount} {chain_native.upper()} will be borrowed for initial liquidity.\n\n"
            f"Please enter the loan duration (in days) as a number no higher than {bot.MAX_LOAN_LENGTH}:"
        )
    )
    return STAGE_DURATION


async def stage_duration(update: Update, context: CallbackContext) -> int:
    duration_input = update.message.text.strip()

    if not (duration_input.isdigit() and 1 <= int(duration_input) <= bot.MAX_LOAN_LENGTH):
        await update.message.reply_text(
            f"Error: Loan duration must be a whole number between 1 and {bot.MAX_LOAN_LENGTH}. Please try again."
        )
        return STAGE_DURATION

    context.user_data['duration'] = int(duration_input)

    await update.message.reply_text(
        text=f"Loan duration will be {context.user_data['duration']} days.\n\n"
             "If the loan is not fully paid before then, it will become eligible for liquidation. "
             "This means the loan amount can be withdrawn from the pair liquidity\n\n"
             "Please provide the address you want ownership transferred to\n\n"
             "This address will be the owner of the token and liquidity tokens\n\n"
             "You can renounce the contract after deployment"
    )
    return STAGE_OWNER


async def stage_contribute(update: Update, context: CallbackContext) -> int:
    native_amount = update.message.text.strip()

    try:
        contribution = Decimal(native_amount)

        if contribution <= 0:
            await update.message.reply_text("Error: The amount must be greater than 0")
            return STAGE_CONTRIBUTE

        if contribution.as_tuple().exponent < -18:
            await update.message.reply_text(
                "Error: Amount cannot have more than 18 decimal places"
            )
            return STAGE_CONTRIBUTE

    except InvalidOperation:
        await update.message.reply_text("Error: Please enter a valid numeric amount")
        return STAGE_CONTRIBUTE

    context.user_data['contribution'] = contribution
    chain_native = chains.chains[context.user_data["chain"]].native

    await update.message.reply_text(
        f"{contribution} {chain_native.upper()} will be allocated for initial liquidity\n\n"
        "Please provide the address you want ownership transferred to\n\n"
        "This address will be the owner of the token and liquidity tokens\n\n"
        "You can renounce the contract after deployment"
    )
    return STAGE_OWNER


async def stage_owner(update: Update, context: CallbackContext) -> int:
    context.user_data['owner'] = update.message.text
    if not is_checksum_address(context.user_data['owner']) \
        or context.user_data['owner'] == ca.DEAD or context.user_data['owner'] == ca.ZERO:
        await update.message.reply_text("Error: Invalid address - Please enter a valid checksum address")
        return STAGE_OWNER
    
    user_data = context.user_data
    
    if 'contribution' in user_data:
        contribution = user_data['contribution']
        ticker = user_data.get('ticker')
        name = user_data.get('name')
        chain = user_data.get('chain')
        supply = user_data.get('supply')
        percent = user_data.get('percent')
        address = user_data.get('owner')
        description = user_data.get('description')
        twitter = user_data.get('twitter')
        telegram = user_data.get('telegram')
        website = user_data.get('website')
        buy_tax = user_data.get('buy_tax')
        sell_tax = user_data.get('sell_tax')

        if all([ticker, name, chain, supply, percent, contribution, address, buy_tax, sell_tax]):
            chain_info = chains.chains[chain]

            team_tokens = int(supply) * (int(percent) / 100)
            liquidity_tokens = int(supply) - team_tokens

            price_native = float(contribution) / liquidity_tokens
            price_usd = price_native * chainscan.get_native_price(chain.lower()) * 2
            market_cap_usd = price_usd * int(supply) * 2

            supply_float = float(supply)
            amount_percentage = float(percent) / 100
            team_supply = supply_float * amount_percentage
            liquidity_supply = supply_float - team_supply

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes", callback_data="confirm_yes")],
                [InlineKeyboardButton("No", callback_data="confirm_no")]
            ])

            await update.message.reply_text(
                f"Thank you! Please check the values below:\n\n"
                f"Chain: {chain.upper()}\n"
                f"Ticker: {ticker}\n"
                f"Project Name: {name}\n"
                f"Description: {description}\n"
                f"Twitter: {twitter}\n"
                f"Telegram: {telegram}\n"
                f"Website: {website}\n"
                f"Taxes: {buy_tax}/{sell_tax}\n"
                f"Total Supply: {supply_float:,.0f}\n"
                f"Team Supply: {team_supply:,.0f} ({percent}%)\n"
                f"Liquidity Supply: {liquidity_supply:,.0f}\n"
                f"Contribution: {contribution} {chain_info.native.upper()}\n\n"
                f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
                f"Ownership of the project will be transferred to:\n`{address}`\n\n"
                "Do you want to proceed with the launch?",
            parse_mode="Markdown",
            reply_markup=buttons
            )
            return STAGE_CONFIRM
        else:
            await update.message.reply_text("Error: Incomplete information provided")
            return ConversationHandler.END
    
    else:
        ticker = user_data.get('ticker')
        name = user_data.get('name')
        chain = user_data.get('chain')
        supply = user_data.get('supply')
        percent = user_data.get('percent')
        loan = user_data.get('loan')
        duration = user_data.get('duration')
        address = user_data.get('owner')
        description = user_data.get('description')
        twitter = user_data.get('twitter')
        telegram = user_data.get('telegram')
        website = user_data.get('website')
        buy_tax = user_data.get('buy_tax')
        sell_tax = user_data.get('sell_tax')

        if all([ticker, name, chain, supply, percent, loan, duration, address, buy_tax, sell_tax]):
            chain_info = chains.chains[chain]

            fee, _ = tools.generate_loan_terms(chain, loan)
            context.user_data['fee'] = fee

            team_tokens = int(supply) * (int(percent) / 100)
            liquidity_tokens = int(supply) - team_tokens

            price_native = float(loan) / liquidity_tokens
            price_usd = price_native * chainscan.get_native_price(chain.lower()) * 2
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
                f"Chain: {chain.upper()}\n"
                f"Ticker: {ticker}\n"
                f"Project Name: {name}\n"
                f"Description: {description}\n"
                f"Twitter: {twitter}\n"
                f"Telegram: {telegram}\n"
                f"Website: {website}\n"
                f"Taxes: {buy_tax}/{sell_tax}\n"
                f"Total Supply: {supply_float:,.0f}\n"
                f"Team Supply: {team_supply:,.0f} ({percent}%)\n"
                f"Loan Supply: {loan_supply:,.0f}\n"
                f"Loan Amount: {loan} {chain_info.native.upper()}\n"
                f"Loan Duration: {duration} Days\n"
                f"Cost: {chain_info.w3.from_wei(fee, 'ether')} {chain_info.native.upper()}\n\n"
                f"Launch Market Cap: ${market_cap_usd:,.0f}\n\n"
                f"Ownership of the project will be transferred to:\n`{address}`\n\n"
                "Do you want to proceed with the launch?",
            parse_mode="Markdown",
            reply_markup=buttons
            )
            return STAGE_CONFIRM
        else:
            await update.message.reply_text("Error: Incomplete information provided")
            return ConversationHandler.END
        

async def stage_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_data = context.user_data
    confirm = query.data.split('_')[1]
    user = update.effective_user
    user_name = user.username or f"{user.first_name} {user.last_name}"
    user_id = user.id
    
    if confirm == "yes":
        account = Account.create()
        now = datetime.now()

        chain = user_data.get('chain')
        chain_info = chains.chains[chain]

        def message(total_cost):
            return (f"On {chain_info.name.upper()}. Send {round(chain_info.w3.from_wei(total_cost, "ether"), 4)} {chain_info.native.upper()} (This includes gas fees) to the following address:\n\n"
                    f"`{account.address}`\n\n"
                    "Any fees not used will be returned to the wallet you designated as owner at deployment\n\n"
                    "*Ensure you are sending funds on the correct chain\n\n"
                    "Make a note of the wallet address above and private key below*\n\n"
                    f"`{account.key.hex()}`\n\n"
                    "To check the status of your launch use /status")

        if 'contribution' in user_data:
            fee = user_data.get('contribution') * 10 ** 18
            gas_estimate = functions.estimate_gas_without_loan(
                    user_data.get('chain'),
                    user_data.get('name'),
                    user_data.get('ticker'),
                    user_data.get('supply'),
                    user_data.get('percent'),
                    user_data.get('description'),
                    user_data.get('twitter'),
                    user_data.get('telegram'),
                    user_data.get('website'),
                    user_data.get('buy_tax'),
                    user_data.get('sell_tax'),
                    user_data.get('owner'),
                    int(fee)
                    )
            if isinstance(gas_estimate, str) and gas_estimate.startswith("Error"):
                await query.message.reply_text(f"{gas_estimate}")
                return

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
                user_data.get('description'),
                user_data.get('twitter'),
                user_data.get('telegram'),
                user_data.get('website'),
                user_data.get('buy_tax'),
                user_data.get('sell_tax'),
                0,
                0,
                user_data.get('owner'),
                int(fee)
            )

        else:
            fee = user_data.get('fee')
            gas_estimate = functions.estimate_gas_with_loan(
                user_data.get('chain'),
                user_data.get('name'),
                user_data.get('ticker'),
                user_data.get('supply'),
                user_data.get('percent'),
                user_data.get('description'),
                user_data.get('twitter'),
                user_data.get('telegram'),
                user_data.get('website'),
                user_data.get('buy_tax'),
                user_data.get('sell_tax'),
                chain_info.w3.to_wei(user_data.get('loan'), 'ether'),
                int(user_data.get('duration')) * 60 * 60 * 24,
                user_data.get('owner'),
                int(fee)
                )
            if isinstance(gas_estimate, str) and gas_estimate.startswith("Error"):
                await query.message.reply_text(f"{gas_estimate}")
                return
             
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
                user_data.get('description'),
                user_data.get('twitter'),
                user_data.get('telegram'),
                user_data.get('website'),
                user_data.get('buy_tax'),
                user_data.get('sell_tax'),
                user_data.get('loan'),
                user_data.get('duration'), 
                user_data.get('owner'),
                int(fee)
            )

        total_cost = (int(fee) + gas_estimate)

        await query.message.reply_text(
            message(total_cost),
        parse_mode="Markdown"
        )
        return ConversationHandler.END

    elif confirm == "no":
        db.delete_entry(user_id)
        await query.message.reply_text("Project canceled. You can start over with /launch")
        return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Launch canceled.")
    return ConversationHandler.END


async def with_loan(update: Update, context: CallbackContext) -> int:
    await function(update, context, with_loan=True)


async def without_loan(update: Update, context: CallbackContext) -> int:
    await function(update, context, with_loan=False)


async def function(update: Update, context: CallbackContext, with_loan: bool) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    status_text = db.search_entry(user_id)
    
    if not status_text:
        await query.edit_message_text("No deployment status found")
        return
    
    chain = status_text["chain"]
    chain_info = chains.chains[chain]
    
    await query.edit_message_text(
        f"Deploying {status_text['ticker']} ({status_text['chain']})...."
    )

    loan_button = None

    if with_loan:
        loan_contract = bot.LIVE_LOAN(chain, "address")

        loan = functions.deploy_token_with_loan(
            status_text["chain"],
            status_text["name"],
            status_text["ticker"],
            int(status_text["supply"]),
            int(status_text["percent"]),
            status_text["description"], 
            status_text["twitter"], 
            status_text["telegram"],
            status_text["website"],
            status_text["buy_tax"],
            status_text["sell_tax"],
            chain_info.w3.to_wei(status_text["loan"], 'ether'),
            int(status_text["duration"]) * 60 * 60 * 24,
            status_text["owner"],
            status_text["address"],
            status_text["secret_key"],
            int(status_text["fee"])
        )

        if isinstance(loan, str) and loan.startswith("Error"):
            await query.edit_message_text(f"Error initiating TX\n\nuse /withdraw if you want to cancel the deployment and return your funds\n\n{loan}")
            return

        token_address, pair_address, loan_id = loan

        try:
            contract = chain_info.w3.eth.contract(address=chain_info.w3.to_checksum_address(loan_contract), 
                                         abi=chainscan.get_abi(loan_contract, chain))
            schedule1 = contract.functions.getPremiumPaymentSchedule(int(loan_id)).call()
            schedule2 = contract.functions.getPrincipalPaymentSchedule(int(loan_id)).call()
            schedule = tools.format_schedule(schedule1, schedule2, chain_info.native.upper())
        except Exception:
            schedule = "Unavailable"

        try:
            token_by_id = None
            index = 0
            
            while True:
                try:
                    token_id = contract.functions.tokenByIndex(index).call()
                    if token_id == int(loan_id):
                        token_by_id = index
                        break
                    index += 1

                except Exception:
                    break

        except Exception:
            token_by_id = None

        message_text = (
            f"Congratulations {status_text['ticker']} has been launched and an Xchange ILL Created on {chain_info.name}\n\n"
            f"CA: `{token_address}`\n\n"
            f"Loan ID: {loan_id}\n\n"
            f"Payment Schedule:\n\n"
            f"{schedule}\n\n"
            f"Your wallet:\n"
            f"`{status_text['owner']}`\n\n"
            f"Has the ability to:\n"
            f"- Change the taxes\n"
            f"- Update the tax wallet\n"
            f"- Adjust the fee thresholds\n"
            f"- Renounce the contract\n\n"
            f"Use the 'Token Contract' button below"
        )

        loan_button = InlineKeyboardButton(text="View Loan", url=f"{urls.XCHANGE}lending/{chain_info.short_name}/{bot.LIVE_LOAN(chain, "name")}/{token_by_id}")

    else:
        launched = functions.deploy_token_without_loan(
            status_text["chain"],
            status_text["name"],
            status_text["ticker"],
            int(status_text["supply"]),
            int(status_text["percent"]),
            status_text["description"], 
            status_text["twitter"], 
            status_text["telegram"],
            status_text["website"],
            status_text["buy_tax"],
            status_text["sell_tax"],
            status_text["owner"],
            status_text["address"],
            status_text["secret_key"],
            int(status_text["fee"])
        )

        if isinstance(launched, str) and launched.startswith("Error"):
            await query.edit_message_text(f"Error initiating TX\n\nUse /withdraw if you want to cancel the deployment and return your funds\n\n{launched}")
            return

        token_address, pair_address = launched

        message_text = (
            f"Congratulations {status_text['ticker']} has been launched and liquidity has been added\n\n"
            f"CA: `{token_address}`\n\n"
            f"Your wallet:\n"
            f"`{status_text['owner']}`\n\n"
            f"Has the ability to:\n"
            f"- Change the taxes\n"
            f"- Update the tax wallet\n"
            f"- Adjust the fee thresholds\n"
            f"- Renounce the contract\n\n"
            f"Use the 'Token Contract' button below"
        )
    
    refund = functions.transfer_balance(
        status_text["chain"],
        status_text["address"],
        status_text["owner"],
        status_text["secret_key"]
    )

    if isinstance(refund, str) and refund.startswith("Error"):
        refund_text = f"Error returning funds\n\nThis is likely because you sent close to the perfect amount for gas\n\nUse /withdraw to double check"
    else:
        refund_text = (
            "Funds returned\n\n"
            f"{chain_info.scan_tx}{refund}"
        )

    buttons = [
        [InlineKeyboardButton(text="Token Contract", url=chain_info.scan_token + token_address)],
        [InlineKeyboardButton(text="Pair Contract", url=chain_info.address + pair_address)],
        [InlineKeyboardButton(text="Buy Link", url=urls.XCHANGE_BUY(chain_info.id, token_address))],
        [InlineKeyboardButton(text="Chart", url=urls.DEX_TOOLS(chain_info.dext, token_address))]
    ]

    if loan:
        buttons.append([loan_button])

    message = await query.edit_message_text(
        message_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    try:
        await context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=message.id)
    except Exception as e:
        pass

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=refund_text
    )

    db.set_complete(status_text["user_id"])