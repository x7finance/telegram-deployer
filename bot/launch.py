from telegram import *
from telegram.ext import *
from eth_utils import is_checksum_address

from constants import chains

STAGE_CHAIN, STAGE_TICKER, STAGE_NAME, STAGE_SUPPLY, STAGE_PORTAL, STAGE_WEBSITE, STAGE_WALLET, STAGE_LOAN = range(8)

live_chains = {key: value for key, value in chains.chains.items() if value.live}
live_chain_list = "\n".join([key.upper() for key in live_chains.keys()])

async def command(update: Update, context: CallbackContext) -> int:
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            f"Lets get you setup! by answering a few questions about your project...\n\n"
            f"First, select your chain\n\nSupported Chains:\n{live_chain_list}\n\n"
            f"Or use /cancel to stop the setup.")
        return STAGE_CHAIN

async def stage_chain(update: Update, context: CallbackContext) -> int:
    context.user_data['chain'] = update.message.text.upper()
    if context.user_data['chain'].lower() not in live_chains:
        await update.message.reply_text(f"Error Chain Not Found:\n\nSupported Chains:\n{live_chain_list}")
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
        f"{context.user_data['name']}\n\nGot it! Now, what's the total supply of your token?")
    return STAGE_SUPPLY

async def stage_supply(update: Update, context: CallbackContext) -> int:
    context.user_data['supply'] = update.message.text
    if not context.user_data['supply'].isdigit():
        await update.message.reply_text("Error: Supply should be a numeric value. Please enter the total supply of your token.")
        return STAGE_SUPPLY
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
        return STAGE_WALLET

async def stage_wallet(update: Update, context: CallbackContext) -> int:
    context.user_data['address'] = update.message.text
    if not is_checksum_address(context.user_data['address']):
        await update.message.reply_text("Error: Invalid Ethereum address. Please enter a valid checksum address.")
        return STAGE_WALLET
    else:
        await update.message.reply_text(
            f"`{context.user_data['address']}`\n\nGot it!\n\n"
            "Do you want to boost your launch with a 1 ETH initial liquidity loan?\n\n"
            "The loan repayment will automatically be taken from the liquidity after 7 days unless you decide to pay it back sooner.\n\n"
            "Reply Yes or No",
            parse_mode="Markdown"
            )
    return STAGE_LOAN

async def stage_loan(update: Update, context: CallbackContext) -> int:
    context.user_data['loan'] = update.message.text
    if context.user_data['loan'].lower() == "yes" or context.user_data['loan'].lower() == "no":
        await stage_complete(context.user_data, update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Reply yes or No")
        return STAGE_LOAN


async def stage_complete(user_data, update, context):
    ticker = user_data.get('ticker')
    name = user_data.get('name')
    chain = user_data.get('chain')
    supply = user_data.get('supply')
    portal = user_data.get('portal')
    website = user_data.get('website')
    address = user_data.get('address')
    loan = user_data.get('loan')
    if loan == "yes":
        loan_text = "Project will be launched with 1 ETH Initial Liquidity"
    else:
        loan_text = ""
    if name and ticker:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "Thank you, Please check the values below\n\n"
                f"Chain: {chain}\n"
                f"Ticker: {ticker}\n"
                f"Project Name: {name}\n"
                f"Supply: {supply}\n"
                f"Portal: {portal}\n"
                f"Website: {website}\n"
                f"{loan_text}\n"
                f"Ownership of the project will be transfered to:\n`{address}`\n\n"
                "If the details are correct hit the launch button!"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"LAUNCH!", url=f"x7finance.org"
                        )
                    ]
                ]
            ),
        )
    else:
        await update.message.reply_text("Error: Incomplete information provided.")


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'Conversation canceled. /start to begin again.')
    return ConversationHandler.END