from constants import bot, chains

from datetime import datetime, timedelta
from web3 import Web3
import unicodedata


def datetime_to_timestamp(datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        timestamp = datetime_obj.timestamp()
        return timestamp
    except ValueError:
        return "Invalid datetime format. Please use YYYY-MM-DD HH:MM."
    

def escape_markdown(text):
    characters_to_escape = ['*', '_', '`']
    for char in characters_to_escape:
        text = text.replace(char, '\\' + char)
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
        value1 = next((v for d, v in zip(schedule1[0], schedule1[1]) if d == date), 0)
        value2 = next((v for d, v in zip(schedule2[0], schedule2[1]) if d == date), 0)

        total_value = value1 + value2

        formatted_date = format_date(date)
        formatted_value = total_value / 10**18
        sch = f"{formatted_date} - {formatted_value:.3f} {native_token}"
        schedule_list.append(sch)

        if datetime.fromtimestamp(date) > current_datetime:
            if next_payment_datetime is None or datetime.fromtimestamp(date) < next_payment_datetime:
                next_payment_datetime = datetime.fromtimestamp(date)
                next_payment_value = formatted_value

    if next_payment_datetime:
        time_until_next_payment = next_payment_datetime - current_datetime
        time_remaining_str = calculate_time_remaining_str(time_until_next_payment)

        schedule_list.append(f"\nNext Payment Due:\n{next_payment_value} {native_token}\n{time_remaining_str}")

    return "\n".join(schedule_list)


def generate_loan_terms(chain, loan_amount):
    chain_native = chains.chains[chain].token
    chain_web3 = chains.chains[chain].w3
    web3 = Web3(Web3.HTTPProvider(chain_web3))
    loan_in_wei = web3.to_wei(loan_amount, 'ether')
    current_loan_version = bot.LOANS.get(bot.LIVE_LOAN)
    origination_fee = current_loan_version['origination_fee'](loan_in_wei)
    cost_string = current_loan_version['cost_string']
    if callable(cost_string):
        cost_string = cost_string(chain_native)
    loan_ca = current_loan_version['contract'](chain)
    loan_deposit = web3.to_wei(bot.LIQUIDATION_DEPOSIT, 'ether')
    fee = origination_fee + loan_deposit
    text = f"Borrow up to {bot.MAX_LOAN_AMOUNT} {chain_native.upper()} liquidity for {cost_string} + {bot.LIQUIDATION_DEPOSIT} {chain_native.upper()} deposit"

    return fee, loan_ca, text


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


def detect_emojis(text):
    for char in text:
        if unicodedata.category(char) in {'Ll', 'Lu', 'Nd'}:
            return False
    return True


def split_message(message: str, max_length: int = 4096) -> list:
    parts = []
    while len(message) > max_length:
        split_at = message.rfind('\n', 0, max_length)
        if split_at == -1:
            split_at = message.rfind(' ', 0, max_length)
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
        datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M')
        return datetime_str
    except ValueError:
        return "Invalid timestamp."