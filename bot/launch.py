from telegram import *
from telegram.ext import *
from eth_utils import is_checksum_address
from eth_account import Account
from datetime import datetime

from constants import chains, bot
from hooks import db

import setup

STAGE_CHAIN, STAGE_TICKER, STAGE_NAME, STAGE_SUPPLY, STAGE_PORTAL, STAGE_WEBSITE, STAGE_OWNER, STAGE_CONFIRM = range(8)


live_chains = {key: value for key, value in chains.chains.items() if value.live}
live_chain_list = "\n".join([key.upper() for key in live_chains.keys()])


async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        user_id = update.effective_user.id
        status_text = db.search_entry_by_user_id(user_id)
        if status_text:
            await update.message.reply_text(
                f"Currently awaiting launch for {status_text["ticker"]} ({status_text["chain"]})\n\n"
                f"Fund `{status_text["address"]}` with {bot.LOAN_FEE} ETH\n\n"
                f"Ownership will be transfered to:\n{status_text["owner"]}\n\n"
                f"To clear this deployment use /reset",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"Lets get you launched by answering a few questions about your project...\n\n"
                f"First, select your chain\n\nCurrent Supported Chains:\n{live_chain_list}\n\n"
                f"Or use /cancel to stop the launch.")
            return STAGE_CHAIN
        


async def stage_chain(update: Update, context: CallbackContext) -> int:
    context.user_data['chain'] = update.message.text.upper()
    if context.user_data['chain'].lower() not in live_chains:
        await update.message.reply_text(f"Error: Chain Not Found\n\nSupported Chains:\n{live_chain_list}")
        return STAGE_CHAIN
    else:
        await update.message.reply_text(
            f"{context.user_data['chain']}\n\nBrilliant! Now, what's the project's token ticker?")
        return STAGE_TICKER


async def stage_ticker(update: Update, context: CallbackContext) -> int:
    context.user_data['ticker'] = update.message.text
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
        f"{context.user_data['supply']}\n\nThanks! Now, what's your project's Telegram Group Portal Link?")
    return STAGE_PORTAL


async def stage_portal(update: Update, context: CallbackContext) -> int:
    context.user_data['portal'] = update.message.text
    if not context.user_data['portal'].startswith('t.me/'):
        await update.message.reply_text("Error: Portal link should start with t.me/, please try again.")
        return STAGE_PORTAL
    else:
        await update.message.reply_text(
            f"{context.user_data['portal']}\n\nThanks! Now, what's your project's website? If you don't have one, reply 'None'.")
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
                    f"Pair will be launched with 1 ETH Initial Liquidity, the loan will be paid back via liqudity after 7 days unless paid back sooner!\n\n"
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
                                        f'Please note: This wallet will expire after {bot.DELETE_HOURS} hours, to check the status of your launch use /status',
                parse_mode="Markdown")
        return ConversationHandler.END


    elif user_response == "no":
        await update.message.reply_text("Deployment cancelled. You can start over with /launch.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please reply with 'yes' or 'no'.")
        return STAGE_CONFIRM


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("launch canceled.")
    return ConversationHandler.END