from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from constants.bot import settings, urls
from constants.protocol import abis, chains
from utils import onchain, tools
from services import get_dbmanager, get_etherscan

db = get_dbmanager()
etherscan = get_etherscan()


async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    launch_type = query.data

    user_id = update.effective_user.id
    status_text = await db.search_entry(user_id)

    if not status_text:
        await query.edit_message_text("No deployment status found")
        return

    chain = status_text["chain"]
    chain_info = await chains.get_chain_info(chain)
    dex_info = chains.DEXES[status_text["dex"]]

    await query.edit_message_text(
        f"Deploying {status_text['ticker']} on {status_text['dex'].upper()} ({chain_info.name.upper()})...."
    )

    loan_button = None
    loan_text = ""

    if launch_type == "launch_with_loan":
        loan_contract = settings.live_loan(chain, "address")

        loan = await onchain.deploy_token_with_loan(
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
            chain_info.w3.to_wei(status_text["loan"], "ether"),
            int(status_text["duration"]) * 60 * 60 * 24,
            status_text["owner"],
            status_text["address"],
            status_text["secret_key"],
            int(status_text["fee"]),
        )

        if isinstance(loan, str) and loan.startswith("Error"):
            await query.edit_message_text(
                f"Error initiating TX\n\nuse /withdraw if you want to cancel the deployment and return your funds\n\n{loan}"
            )
            return

        token_address, pair_address, loan_id = loan

        try:
            contract = chain_info.w3.eth.contract(
                address=chain_info.w3.to_checksum_address(loan_contract),
                abi=abis.read("ill005"),
            )
            schedule1 = await contract.functions.getPremiumPaymentSchedule(
                int(loan_id)
            ).call()
            schedule2 = await contract.functions.getPrincipalPaymentSchedule(
                int(loan_id)
            ).call()
            schedule = tools.format_schedule(
                schedule1, schedule2, chain_info.native.upper()
            )
        except Exception:
            schedule = "Unavailable"

        try:
            token_by_id = None
            index = 0

            while True:
                try:
                    token_id = await contract.functions.tokenByIndex(
                        index
                    ).call()
                    if token_id == int(loan_id):
                        token_by_id = index
                        break
                    index += 1

                except Exception:
                    break

        except Exception:
            token_by_id = None

        loan_button = InlineKeyboardButton(
            text="Manage Loan",
            url=f"{dex_info.url}lending/{chain_info.short_name}/{settings.live_loan(chain, 'name')}/{token_by_id}",
        )

        loan_text = (
            f"Loan ID: {loan_id}\n\nPayment Schedule:\n\n{schedule}\n\n"
        )

    elif launch_type == "launch_without_loan":
        launched = await onchain.deploy_token_without_loan(
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
            int(status_text["fee"]),
        )

        if isinstance(launched, str) and launched.startswith("Error"):
            await query.edit_message_text(
                f"Error initiating TX\n\nUse /withdraw if you want to cancel the deployment and return your funds\n\n{launched}"
            )
            return

        token_address, pair_address = launched

    elif launch_type == "launch_uniswap":
        launched = await onchain.deploy_token(
            status_text["chain"],
            status_text["name"],
            status_text["ticker"],
            int(status_text["supply"]),
            int(status_text["percent"]),
            status_text["buy_tax"],
            status_text["sell_tax"],
            status_text["owner"],
            status_text["address"],
            status_text["secret_key"],
            int(status_text["fee"]),
        )

        if isinstance(launched, str) and launched.startswith("Error"):
            await query.edit_message_text(
                f"Error initiating TX\n\nUse /withdraw if you want to cancel the deployment and return your funds\n\n{launched}"
            )
            return

        token_address, pair_address = launched

    refund = await onchain.transfer_balance(
        status_text["chain"],
        status_text["address"],
        status_text["owner"],
        status_text["secret_key"],
    )

    if isinstance(refund, str) and refund.startswith("Error"):
        refund_text = (
            f"No funds returned\n\n{refund}\n\n"
            "If this is unexpected use your saved private key from setup to withdraw funds"
        )
    else:
        refund_text = f"Funds returned\n\n{chain_info.scan_tx}{refund}"

    message_text = (
        f"Congratulations {status_text['ticker']} has been launched on {status_text['dex'].upper()} ({chain_info.name.upper()})\n\n"
        f"CA: `{token_address}`\n\n"
        f"Your wallet:\n"
        f"`{status_text['owner']}`\n\n"
        f"{loan_text}"
        f"Has the ability to:\n"
        f"- Change the taxes\n"
        f"- Change the tax wallet\n"
        f"- Change the fee thresholds\n"
        f"- Renounce the contract\n\n"
        f"Use the 'Manage Token' button below"
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Buy Link",
                url=urls.xchange_buy(chain_info.id, token_address),
            )
        ],
        [
            InlineKeyboardButton(
                text="Chart Link",
                url=urls.dex_tools_link(chain_info.dext, token_address),
            )
        ],
        [
            InlineKeyboardButton(
                text="Manage Token", url=f"{urls.XCHANGE}create?tab=manage"
            )
        ],
        [
            InlineKeyboardButton(
                text="Manage Liquidity", url=dex_info.url + dex_info.liq_link
            )
        ],
    ]

    if loan_button:
        buttons.append([loan_button])

    message = await query.edit_message_text(
        message_text,
        message_effect_id="5046509860389126442",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    try:
        await context.bot.pin_chat_message(
            chat_id=update.effective_chat.id, message_id=message.id
        )
    except Exception:
        pass

    await context.bot.send_message(
        chat_id=query.message.chat_id, text=refund_text
    )

    await db.set_complete(status_text["user_id"])


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if query.data == "reset_yes":
        delete_text = await db.delete_entry(user_id)
        if delete_text:
            await query.edit_message_text(
                "Project reset. Use /launch to start a new project"
            )
        else:
            await query.edit_message_text(
                "No projects waiting, please use /launch to start"
            )
    elif query.data == "reset_no":
        await query.edit_message_text("Reset canceled.")


HANDLERS = [
    (launch, r"^(launch_uniswap|launch_with_loan|launch_without_loan)$"),
    (reset, "^reset_"),
]
