from database import Chats
from tools.logger import logger
from pyrogram import Client
from pyrogram.errors import MessageDeleteForbidden, ChatAdminRequired, ChatNotModified, ChatRestricted, FloodWait, MediaEmpty, ChannelPrivate, MessageIdInvalid, TopicClosed
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools.tools import status_lock, IST
from tools.enums import Messages, full_lock_permissions


async def _process_shabat_groups(client: Client, groups: list[dict], is_locking: bool, holiday_name: str | None = None):
    """
    Helper function to process groups for Shabbat and holiday locking/unlocking
    """
    count = 0
    for group in groups:
        messages = Messages(language=group.get("language") or "he")
        chat_id = group.get('chat_id')
        if is_locking:
            permissions = full_lock_permissions
            if holiday_name:
                message = group.get("holiday_message") or messages.holiday_lock.format(holiday_name)
                img_file_id = group.get("holiday_message_img")
            else:
                message = group.get("calendar_message") or messages.shabbat_lock
                img_file_id = group.get("calendar_message_img")
        else:
            permissions = await Chats.get_permissions(chat_id)
            if holiday_name:
                message = group.get("holiday_message") or messages.holiday_unlock
                img_file_id = group.get("holiday_message_img")
            else:
                message = group.get("havdalah_message") or messages.shabbat_unlock
                img_file_id = group.get("havdalah_message_img")
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
            await Chats.update(chat_id, temp_message_id=msg.id)
            await asyncio.sleep(2)
        except TopicClosed:
            pass
        except FloodWait as e:
            try:
                await asyncio.sleep(e.value)
                await client.set_chat_permissions(chat_id, permissions)
                msg = await client.send_message(chat_id, message)
                await Chats.update(chat_id, temp_message_id=msg.id)
            except Exception as e:
                logger.error(e)
        except MediaEmpty:
            if is_locking:
                await Chats.update(chat_id, calendar_message_img=None)
            else:
                await Chats.update(chat_id, havdalah_message_img=None)
        except (ChannelPrivate):
            await Chats.update(chat_id, register=False, is_active=False)
        except ChatAdminRequired:
            await Chats.update(chat_id, register=False)
        except (ChatNotModified, ChatRestricted):
            pass
        except Exception as e:
            logger.error(e)
    return count, len(groups)


async def lock_shabat(client: Client, holiday_name: str | None = None):
    """Lock groups for Shabbat"""
    groups = await Chats.get_by(is_admin=True, register=True)
    if not groups:
        return

    count, total = await _process_shabat_groups(client, groups, is_locking=True, holiday_name=holiday_name)
    logger.info("Shabbat locked for {}/{} groups".format(count, total))


async def unlock_shabat(client: Client, holiday_name: str | None = None):
    """Unlock groups after Shabbat"""
    groups = await Chats.get_by(is_admin=True, register=True)
    if not groups:
        return
    count, total = await _process_shabat_groups(client, groups, is_locking=False, holiday_name=holiday_name)
    logger.info("Shabbat unlocked for {}/{} groups".format(count, total))


async def shabat_scheduler(client: Client):
    scheduler = AsyncIOScheduler()
    status = await status_lock()
    if status.get("status") is None:
        return
    elif status.get("status"):
        times_lock = status.get("time")
        scheduler.add_job(lock_shabat, trigger='cron', args=[client, status.get("holiday")], hour=times_lock.hour, minute=times_lock.minute, timezone=IST)
        logger.info("shabat scheduled to {}".format(times_lock.strftime('%H:%M')))
    elif not status.get("status"):
        time_unlock = status.get("time")
        scheduler.add_job(unlock_shabat, trigger='cron', args=[client, status.get("holiday")], hour=time_unlock.hour, minute=time_unlock.minute, timezone=IST)
        logger.info("exit shabat scheduled to {}".format(time_unlock.strftime('%H:%M')))
    scheduler.start()
    return
