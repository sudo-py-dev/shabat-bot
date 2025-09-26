from pyrogram import Client, filters, idle
from pyrogram.types import Message
from database import GroupPermission, Chats
from pyrogram.errors import ChatWriteForbidden, TopicClosed, BadMsgNotification
from tools import join_button, IST, is_admin_msg
from schaduler import shabat_scheduler
from dotenv import load_dotenv
import os
from logger import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from enums import Messages

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("shabat_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("register") & filters.group)
@is_admin_msg()
async def handle_register_chat(_: Client, message: Message):
    chat_id = message.chat.id
    GroupPermission.update(chat_id, message.chat.permissions)
    try:
        if Chats.enable_shabat(chat_id):
            await message.reply(Messages.register_message.value)
        else:
            await message.reply(Messages.unregister_message.value)
    except ValueError as e:
        await message.reply(str(e))
    except (ChatWriteForbidden, TopicClosed):
        pass
    except Exception as e:
        logger.error(e)

@app.on_message(filters.command("permission") & filters.group)
@is_admin_msg()
async def handle_permission(_: Client, message: Message):
    chat_id = message.chat.id
    GroupPermission.update(chat_id, message.chat.permissions)
    try:
        await message.reply(Messages.permission_message.value)
    except (ChatWriteForbidden, TopicClosed):
        pass
    except Exception as e:
        logger.error(e)

@app.on_message(filters.command(["calendar", "כניסה"]) & filters.group)
@is_admin_msg()
async def handle_calendar(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        if not message.reply_to_message:
            await message.reply(Messages.reply_to_set_message.value)
            return
        r_message = message.reply_to_message
        message_text = getattr(r_message, "text", getattr(r_message, "caption", ""))
        if not message_text:
            await message.reply(Messages.reply_to_set_message.value)
            return
        if message_text and hasattr(message_text, "html"):
            message_text = message_text.html

        message_photo = r_message.photo.sizes[-1].file_id if r_message.photo else None
        if Chats.update_message(chat_id, message_text, message_photo, "calendar"):
            await message.reply_to_message.reply(Messages.shabbat_updated.value)
        else:
            await message.reply(Messages.invalid_or_not_existing_group.value)
    except (ChatWriteForbidden, TopicClosed):
        pass
    except Exception as e:
        logger.error(e)


@app.on_message(filters.command(["havdalah", "הבדלה"]) & filters.group)
@is_admin_msg()
async def handle_havdalah(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        if not message.reply_to_message:
            await message.reply(Messages.reply_to_set_message.value)
            return
        r_message = message.reply_to_message
        message_text = getattr(r_message, "text", getattr(r_message, "caption", ""))
        if not message_text:
            await message.reply(Messages.reply_to_set_message.value)
            return
        if message_text and hasattr(message_text, "html"):
            message_text = message_text.html

        message_photo = r_message.photo.sizes[-1].file_id if r_message.photo else None
        if Chats.update_message(chat_id, message_text, message_photo, "havdalah"):
            await message.reply_to_message.reply(Messages.havdalah_updated.value)
        else:
            await message.reply(Messages.invalid_or_not_existing_group.value)
    except (ChatWriteForbidden, TopicClosed):
        pass
    except Exception as e:
        logger.error(e)

@app.on_message(filters.command("start") & filters.private)
async def handle_start(client: Client, message: Message):
    try:
        await message.reply(Messages.start_message.value, reply_markup=join_button(client.me.username))
    except Exception as e:
        logger.error(e)

@app.on_message(filters.command("help") & filters.private)
async def handle_help(client: Client, message: Message):
    try:
        await message.reply(Messages.help_message.value)
    except Exception as e:
        logger.error(e)


async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(shabat_scheduler, trigger='cron', args=[app], hour=11, minute=48, timezone=IST) # every day at 13:00 check for shabat scheduler
    scheduler.start()
    return scheduler


async def main():
    await start_scheduler()
    logger.info("BOT START")
    await app.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("User has been interrupted. Exiting...")
    except BadMsgNotification:
        logger.error("date and time not correct in your system")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

