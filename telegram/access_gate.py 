# telegram/access_gate.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.error import TelegramError

from .config import OWNER_IDS, REQUIRED_CHANNELS, REQUIRED_GROUPS


async def _is_member(bot, chat, user_id):
    try:
        member = await bot.get_chat_member(chat, user_id)
        return member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except TelegramError:
        return False


async def check_access(bot, user_id):
    # 👑 Owner bypass
    if user_id in OWNER_IDS:
        return [], []

    missing_channels = []
    missing_groups = []

    for channel in REQUIRED_CHANNELS:
        if not await _is_member(bot, channel, user_id):
            missing_channels.append(channel)

    for group in REQUIRED_GROUPS:
        if not await _is_member(bot, group, user_id):
            missing_groups.append(group)

    return missing_channels, missing_groups


def build_join_buttons(missing_channels, missing_groups, page=0, page_size=4):
    items = (
        [("channel", c) for c in missing_channels] +
        [("group", g) for g in missing_groups]
    )

    start = page * page_size
    end = start + page_size
    chunk = items[start:end]

    keyboard = []

    for kind, name in chunk:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📢 Join {name}" if kind == "channel" else f"👥 Join {name}",
                url=f"https://t.me/{name[1:]}"
            )
        ])

    navigation = []
    if start > 0:
        navigation.append(
            InlineKeyboardButton("⬅️ Prev", callback_data=f"gate:{page-1}")
        )
    if end < len(items):
        navigation.append(
            InlineKeyboardButton("Next ➡️", callback_data=f"gate:{page+1}")
        )

    if navigation:
        keyboard.append(navigation)

    return InlineKeyboardMarkup(keyboard)