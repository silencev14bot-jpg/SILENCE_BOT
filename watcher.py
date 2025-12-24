# telegram/watcher.py

from .config import REQUIRED_CHANNELS, REQUIRED_GROUPS


async def watch_membership(update, context):
    chat = update.chat_member.chat
    user = update.chat_member.from_user
    new_status = update.chat_member.new_chat_member.status

    if new_status in ("left", "kicked"):
        if chat.username:
            tag = f"@{chat.username}"
            if tag in (REQUIRED_CHANNELS + REQUIRED_GROUPS):
                context.application.bot_data.setdefault(
                    "revoked_users", set()
                ).add(user.id)