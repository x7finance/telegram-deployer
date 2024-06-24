from telegram import *
from telegram.ext import *

from eth_utils import is_checksum_address
from eth_account import Account
from datetime import datetime

from constants import bot, chains
from hooks import db

STAGE_CHAIN, STAGE_TICKER, STAGE_NAME, STAGE_SUPPLY, STAGE_PORTAL, STAGE_WEBSITE, STAGE_OWNER, STAGE_CONFIRM = range(8)


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            await update.message.reply_text(
                f"Currently awaiting launch for {status_text['ticker']} ({status_text['chain']})\n\n"
                f"Fund `{status_text['address']}` with {bot.LOAN_FEE} ETH\n\n"
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
        text=
            f"{context.user_data['chain']} Chain\n\nBrilliant! Now, what's the project's token ticker?"
    )
    return STAGE_TICKER


async def stage_ticker(update: Update, context: CallbackContext) -> int:
    context.user_data['ticker'] = update.message.text
    if len(context.user_data['ticker']) > 5:
        await update.message.reply_text(
            "Error: The ticker must be 5 characters or fewer. Please enter a valid ticker.")
        return STAGE_TICKER 
    await update.message.reply_text(
        f"{context.user_data['ticker']}\n\nGreat! Now, please reply with your project name.")
    return STAGE_NAME


async def stage_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        f"{context.user_data['name']}\n\nGot it! Now, what do you want the total supply of your token to be?")
    return STAGE_SUPPLY


async def stage_supply(update: Update, context: CallbackContext) -> int:
    supply_input = update.message.text.strip()
    if not (supply_input.isdigit() and int(supply_input) > 0):
        await update.message.reply_text("Error: Supply should be a whole number greater than zero, with no decimals. Please try again.")
        return STAGE_SUPPLY
    context.user_data['supply'] = supply_input
    await update.message.reply_text(
        f"{context.user_data['supply']} Supply\n\nThanks! Now, what's your project's Telegram Group Portal Link?\n\nIf you don't have one, reply 'None'.")
    return STAGE_PORTAL


async def stage_portal(update: Update, context: CallbackContext) -> int:
    context.user_data['portal'] = update.message.text
    if not context.user_data['portal'].startswith('t.me/') and context.user_data['portal'] != 'None': 
        await update.message.reply_text("Error: Portal link should start with t.me/, please try again.")
        return STAGE_PORTAL
    else:
        await update.message.reply_text(
            f"{context.user_data['portal']}\n\nThanks! Now, what's your project's website?\n\nIf you don't have one, reply 'None'.")
        return STAGE_WEBSITE


async def stage_website(update: Update, context: CallbackContext) -> int:
    context.user_data['website'] = update.message.text
    if not context.user_data['website'].startswith('http') and context.user_data['website'] != 'None': 
        await update.message.reply_text("Error: Website address should start with 'http', or 'None'. Please try again.")
        return STAGE_WEBSITE
    else:
        await update.message.reply_text(
            f"{context.user_data['website']}\n\nGreat! Now, what's the wallet address you want ownership transferred to?")
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
        portal = user_data.get('portal')
        website = user_data.get('website')
        address = user_data.get('owner')

        if all([name, ticker, chain, supply, portal, website, address]):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "Thank you, Please check the values below\n\n"
                    f"Chain: {chain}\n"
                    f"Ticker: {ticker}\n"
                    f"Project Name: {name}\n"
                    f"Supply: {supply}\n"
                    f"Portal: {portal}\n"
                    f"Website: {website}\n\n"
                    f"Ownership of the project will be transferred to:\n`{address}`\n\n"
                    "Are these details correct?"
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
                      user_data.get('portal'), 
                      user_data.get('website'), 
                      user_data.get('owner')
                      )
        await update.message.reply_text(f'Please send {bot.LOAN_FEE} ETH to the following address:\n\n`{account.address}`.\n\n'
                                        '*Make a note of this wallet address as your reference number*\n\n'
                                        'To check the status of your launch use /status',
                parse_mode="Markdown")
        return ConversationHandler.END

    elif user_response == "no":
        await update.message.reply_text("Project cancelled. You can start over with /project.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please reply with 'yes' or 'no'.")
        return STAGE_CONFIRM


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("launch canceled.")
    return ConversationHandler.END