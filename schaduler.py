import datetime
from database import Chats, GroupPermission
from logger import logger
from pyrogram import Client
from pyrogram.errors import MessageDeleteForbidden, ChatAdminRequired, ChatNotModified, ChatRestricted, FloodWait, MediaEmpty, ChannelPrivate, MessageIdInvalid, TopicClosed
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools import status_lock, IST
from enums import Messages, full_lock


async def _process_shabat_groups(client: Client, groups: list[dict], is_locking: bool, holiday_name: str | None = None):
    """
    Helper function to process groups for Shabbat and holiday locking/unlocking
    """
    count = 0
    for group in groups:
        chat_id = group.get('chat_id')
        if is_locking:
            if holiday_name:
                message = Messages.holiday_lock.value.format(holiday_name)
            else:
                message = group.get("calendar_message") or Messages.shabbat_lock.value
            img_file_id = group.get("calendar_message_img")
            permissions = full_lock
        else:
            if holiday_name:
                message = Messages.holiday_unlock.value
            else:
                message = group.get("havdalah_message") or Messages.shabbat_unlock.value
            img_file_id = group.get("havdalah_message_img")
            permissions = GroupPermission.get(chat_id)
            if (mid := group.get("temp_message_id")) is not None:
                try:
                    await client.delete_messages(chat_id, mid)
                except (MessageDeleteForbidden, MessageIdInvalid):
                    pass
        try:
            await client.set_chat_permissions(chat_id, permissions)
            if img_file_id:
                msg = await client.send_photo(chat_id, img_file_id, caption=message)
            else:
                msg = await client.send_message(chat_id, message)
            count += 1
            Chats.update_one(chat_id, "temp_message_id", msg.id)
            await asyncio.sleep(2)
        except TopicClosed:
            pass
        except FloodWait as e:
            try:
                await asyncio.sleep(e.value)
                await client.set_chat_permissions(chat_id, permissions)
                msg = await client.send_message(chat_id, message)
                Chats.update_one(chat_id, "temp_message_id", msg.id)
            except Exception as e:
                logger.error(e)
        except MediaEmpty:
            if is_locking:
                Chats.update_one(chat_id, "calendar_message_img", None)
            else:
                Chats.update_one(chat_id, "havdalah_message_img", None)
        except (ChannelPrivate, ChatAdminRequired):
            Chats.update_one(chat_id, "enabled", False)
        except (ChatNotModified, ChatRestricted):
            pass
        except Exception as e:
            logger.error(e)
    return count, len(groups)


async def lock_shabat(client: Client, holiday_name: str | None = None):
    """Lock groups for Shabbat"""
    groups = Chats.get_enabled()
    if not groups:
        return

    count, total = await _process_shabat_groups(client, groups, is_locking=True, holiday_name=holiday_name)
    logger.info("Shabbat locked for {}/{} groups".format(count, total))


async def unlock_shabat(client: Client, holiday_name: str | None = None):
    """Unlock groups after Shabbat"""
    groups = Chats.get_enabled()
    if not groups:
        return
    count, total = await _process_shabat_groups(client, groups, is_locking=False, holiday_name=holiday_name)
    logger.info("Shabbat unlocked for {}/{} groups".format(count, total))


async def shabat_scheduler(client: Client):
    scheduler = AsyncIOScheduler()
    status = await status_lock()
    if status[0] is None or len(status) < 3:
        return
    elif status[0] is True:
        times_lock = status[1] - datetime.timedelta(minutes=40)
        scheduler.add_job(lock_shabat, trigger='cron', args=[client, status[2]], hour=times_lock.hour, minute=times_lock.minute, timezone=IST)
        logger.info("shabat scheduled to {}".format(times_lock.strftime('%H:%M')))
    elif status[0] is False:
        time_unlock = status[1]
        scheduler.add_job(unlock_shabat, trigger='cron', args=[client, status[2]], hour=time_unlock.hour, minute=time_unlock.minute, timezone=IST)
        logger.info("exit shabat scheduled to {}".format(time_unlock.strftime('%H:%M')))
    scheduler.start()
    return
