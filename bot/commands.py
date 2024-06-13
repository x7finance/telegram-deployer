from telegram import *
from telegram.ext import *

from hooks import api
from constants import text


async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    user_name = user.username or f"{user.first_name} {user.last_name}"
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            f"Welcome {api.escape_markdown(user_name)} to {api.escape_markdown(text.BOT_NAME)}\n\n"
            "blah blah blah.....\n\n"
            "use /launch to launch your project now!"
        )