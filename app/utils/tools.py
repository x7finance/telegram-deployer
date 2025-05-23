import aiohttp
import os
import socket
import unicodedata
from datetime import datetime, timedelta

from bot import callbacks
from bot.commands import general, admin
from constants.bot import settings
from constants.protocol import abis, chains
from services import get_dbmanager

db = get_dbmanager()


def datetime_to_timestamp(datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        timestamp = datetime_obj.timestamp()
        return timestamp
    except ValueError:
        return "Invalid datetime format. Please use YYYY-MM-DD HH:MM."


def detect_emojis(text):
    for char in text:
        if unicodedata.category(char) in {"Ll", "Lu", "Nd"}:
            return False
    return True


def escape_markdown(text):
    characters_to_escape = ["*", "_", "`"]
    for char in characters_to_escape:
        text = text.replace(char, "\\" + char)
    return text


def format_schedule(schedule1, schedule2, native_token):
    current_datetime = datetime.utcnow()
    next_payment_datetime = None
    next_payment_value = None

    def format_date(date):
        return datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")

    def calculate_time_remaining_str(time_remaining):
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"

    all_dates = sorted(set(schedule1[0] + schedule2[0]))

    schedule_list = []

    for date in all_dates:
        value1 = next(
            (v for d, v in zip(schedule1[0], schedule1[1]) if d == date), 0
        )
        value2 = next(
            (v for d, v in zip(schedule2[0], schedule2[1]) if d == date), 0
        )

        total_value = value1 + value2

        formatted_date = format_date(date)
        formatted_value = total_value / 10**18
        sch = f"{formatted_date} - {formatted_value:.3f} {native_token}"
        schedule_list.append(sch)

        if datetime.fromtimestamp(date) > current_datetime:
            if (
                next_payment_datetime is None
                or datetime.fromtimestamp(date) < next_payment_datetime
            ):
                next_payment_datetime = datetime.fromtimestamp(date)
                next_payment_value = formatted_value

    if next_payment_datetime:
        time_until_next_payment = next_payment_datetime - current_datetime
        time_remaining_str = calculate_time_remaining_str(
            time_until_next_payment
        )

        schedule_list.append(
            f"\nNext Payment Due:\n{next_payment_value} {native_token}\n{time_remaining_str}"
        )

    return "\n".join(schedule_list)


async def generate_loan_terms(chain, loan_amount):
    chain_info = await chains.get_chain_info(chain)

    loan_in_wei = chain_info.w3.to_wei(loan_amount, "ether")

    loan_contract_address = settings.live_loan(chain, "address")

    contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(loan_contract_address),
        abi=abis.read("ill005"),
    )

    quote = await contract.functions.getQuote(loan_in_wei).call()
    origination_fee = quote[1]

    loan_deposit = chain_info.w3.to_wei(settings.LIQUIDATION_DEPOSIT, "ether")
    total_fee = origination_fee + loan_deposit

    text = (
        f"Borrow up to {settings.MAX_LOAN_AMOUNT} {chain_info.native.upper()} liquidity for "
        f"{chain_info.w3.from_wei(origination_fee, 'ether')} + {settings.LIQUIDATION_DEPOSIT} {chain_info.native.upper()} deposit"
    )

    return total_fee, text


def get_duration_years(duration):
    years = duration.days // 365
    months = (duration.days % 365) // 30
    weeks = ((duration.days % 365) % 30) // 7
    days = ((duration.days % 365) % 30) % 7
    return years, months, weeks, days


def get_duration_days(duration):
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes = (remainder % 3600) // 60
    return days, hours, minutes


def is_local():
    ip = socket.gethostbyname(socket.gethostname())
    return (
        ip.startswith("127.") or ip.startswith("192.168.") or ip == "localhost"
    )


async def set_reminders(app):
    reminders = await db.get_reminders()
    total = len(reminders)

    for reminder in reminders:
        due_date = datetime.strptime(
            str(reminder["due"]), "%Y-%m-%d %H:%M:%S.%f"
        )
        job_name = f"reminder_{reminder['user_id']}"

        if due_date < datetime.now():
            continue

        app.job_queue.run_once(
            callbacks.send_reminder,
            when=due_date,
            data=reminder,
            name=job_name,
        )

    return f"✅ Scheduled {total} reminder(s)"


def split_message(message: str, max_length: int = 4096) -> list:
    parts = []
    while len(message) > max_length:
        split_at = message.rfind("\n", 0, max_length)
        if split_at == -1:
            split_at = message.rfind(" ", 0, max_length)
        if split_at == -1:
            split_at = max_length

        parts.append(message[:split_at])
        message = message[split_at:].lstrip()

    parts.append(message)
    return parts


def timestamp_deadline():
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=10)
    future_timestamp = int(future_time.timestamp())

    return future_timestamp


def timestamp_to_datetime(timestamp):
    try:
        datetime_obj = datetime.fromtimestamp(timestamp)
        datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M")
        return datetime_str
    except ValueError:
        return "Invalid timestamp."


async def update_bot_commands():
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/setMyCommands"

    general_commands = [
        {
            "command": cmd[0] if isinstance(cmd, list) else cmd,
            "description": desc,
        }
        for cmd, _, desc in general.HANDLERS
    ]

    admin_commands = [
        {"command": cmd, "description": desc}
        for cmd, _, desc in admin.HANDLERS
    ]

    all_commands = general_commands + admin_commands

    results = []

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            json={"commands": general_commands, "scope": {"type": "default"}},
        ) as response:
            results.append(
                "✅ General commands updated"
                if response.status == 200
                else f"⚠️ Failed to update general commands: {await response.text()}"
            )

        async with session.post(
            url,
            json={
                "commands": all_commands,
                "scope": {
                    "type": "chat",
                    "chat_id": int(os.getenv("TELEGRAM_ADMIN_ID")),
                },
            },
        ) as response:
            results.append(
                "✅ Admin commands updated"
                if response.status == 200
                else f"⚠️ Failed to update admin commands: {await response.text()}"
            )

    return "\n".join(results)
