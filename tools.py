from hebcal_api import Calendar
from datetime import datetime
from pytz import timezone
import re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from enums import AccessPermission
from pyrogram.enums import ChatMembersFilter, ChatType
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import ChatIdInvalid, ChatAdminRequired, ChannelPrivate, ChatIdInvalid, PeerIdInvalid, MessageDeleteForbidden
from cachetools import TTLCache
from functools import wraps


minutes = 60 * 60 * 2
admins_lists = TTLCache(maxsize=1024, ttl=minutes)
IST = timezone('Asia/Jerusalem')


async def status_lock():
    calendar = Calendar()
    now = datetime.now(IST).date()
    events = await calendar.get_events_async(start=now,
                                             end=now,
                                             geonameid=7498240,
                                             major_holidays=True,
                                             special_shabbatot=True)
    for event in events.items:
        holiday = None
        status = None
        time = None
        yom_tov = None

        if event.candle:
            time = event.candle.time
            status = True
        elif event.holiday:
            if event.holiday.yomtov:
                yom_tov = True
            holiday = event.title
        elif event.havdalah:
            time = event.havdalah.time
            status = False
    if yom_tov and status:
        return (None, None, None)
    return (status, time, holiday)


def is_valid_chat_id(chat_id: int) -> bool:
    return re.match(r"^-100\d{5,15}$", str(chat_id)) is not None



def join_button(username: str) -> InlineKeyboardMarkup:
    """
    Create inline buttons:
    1. Invite bot to a group with admin rights
    2. Link to source code repository
    """
    username = username.lstrip("@")

    buttons = [
        [
            InlineKeyboardButton(
                text="➕ הוסף אותי לקבוצה",
                url=f"https://t.me/{username}?startgroup=start&admin=delete_messages+restrict_members"
            )
        ],
        [
            InlineKeyboardButton(
                text="💻 קוד המקור",
                url="https://github.com/sudo-py-dev/shabat-bot"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def is_admin(client: Client,
                   chat_id: int,
                   user_id: int,
                   permission_require: str = "basic") -> AccessPermission:
    """
    Check if a user is an admin of the group and has the required permission.

    :param client: Client instance
    :param chat_id: Chat ID
    :param user_id: User ID
    :param permission_require: Permission required (e.g., "can_restrict_members")
    :return: AccessPermission enum value
    """
    admins = admins_lists.get(chat_id)
    if user_id == chat_id:
        return AccessPermission.ALLOW
    elif admins is None:
        admins = {}
        try:
            async for admin_member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                admin_user_id = admin_member.user.id
                admin_privileges = admin_member.privileges
                admins[admin_user_id] = admin_privileges
            admins_lists[chat_id] = admins
            admin_privileges = admins.get(user_id)
            if admin_privileges is not None:
                if admin_privileges and permission_require == "basic":
                    return AccessPermission.ALLOW
                elif getattr(admin_privileges, permission_require, False):
                    return AccessPermission.ALLOW
                else:
                    return AccessPermission.DENY
            else:
                return AccessPermission.NOT_ADMIN
        except (ChatIdInvalid, ChatAdminRequired, ChannelPrivate, ChatIdInvalid, PeerIdInvalid):
            return AccessPermission.NOT_CONNECTED
        except Exception:
            return AccessPermission.NOT_ADMIN

    admin_privileges = admins.get(user_id)
    if admin_privileges is not None:
        if admin_privileges and permission_require == "basic":
            return AccessPermission.ALLOW
        elif getattr(admin_privileges, permission_require, False):
            return AccessPermission.ALLOW
        else:
            return AccessPermission.DENY
    else:
        return AccessPermission.NOT_ADMIN


def is_admin_msg(permission_require="basic"):
    def function(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            try:
                chat_id = message.chat.id
                user_id = message.from_user.id if message.from_user else message.sender_chat.id
                if message.chat.type in [ChatType.PRIVATE, ChatType.CHANNEL] or chat_id == user_id:
                    await func(client, message)
                else:
                    access = await is_admin(client, chat_id, user_id, permission_require)
                    if access == AccessPermission.ALLOW:
                        return await func(client, message)
                    elif access == AccessPermission.DENY:
                        return
                    elif access == AccessPermission.NOT_CONNECTED:
                        return
                    else:
                        await message.delete()
                        return

            except (MessageDeleteForbidden, ChannelPrivate, ChatIdInvalid):
                pass

        return wrapper

    return function
