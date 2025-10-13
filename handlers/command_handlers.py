from tools.enums import Messages
from tools.inline_keyboards import select_language_buttons
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from tools.tools import with_language, is_admin_message
from database import Chats


@with_language
async def start_handler(client: Client, message: Message, language: str):
    await message.reply(Messages(language=language).start.format(client.me.full_name))


@with_language
async def help_handler(_, message: Message, language: str):
    commands = Messages(language=language).commands
    commands_str = "\n".join([f"/{command} - {description}" for command, description in commands.items()])
    await message.reply(Messages(language=language).help.format(commands_str))


@is_admin_message()
@with_language
async def change_language_handler(_, message: Message, language: str):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        parts = message.text.split(" ")
        supported_langs = ", ".join(Messages().languages())
        if len(parts) != 2:
            error_msg = Messages(language=language).select_language_groups.format(supported_langs)
            await message.reply(error_msg)
            return
        new_lang = parts[1].strip()
        if new_lang not in Messages().languages():
            error_msg = Messages(language=language).language_not_supported.format(new_lang, supported_langs)
            await message.reply(error_msg)
            return

        await Chats.update(chat_id=message.chat.id, language=new_lang)
        await message.reply(Messages(language=new_lang).language_set_groups)
    else:
        await message.reply(Messages(language=language).select_language, reply_markup=select_language_buttons())


@is_admin_message()
@with_language
async def set_messages_handler(_, message: Message, language: str):
    messages = Messages(language=language)
    if not message.reply_to_message:
        await message.reply(messages.must_reply_to_set_messages)
        return
    elif len(message.command) != 2:
        await message.reply(messages.available_commands)
        return
    
    reply_message = message.reply_to_message
    photo_file_id = None
    text = None
    if reply_message.photo:
        photo_file_id = reply_message.photo.file_id
        text = getattr(reply_message.caption, "html", reply_message.caption)
    elif reply_message.text:
        text = getattr(reply_message.text, "html", reply_message.text)
    else:
        await message.reply(messages.text_or_photo_required)
        return
    
    action = message.command[1]
    if action in ("calendar", "שבת"):
        await Chats.update(chat_id=message.chat.id, calendar_message=text, calendar_message_img=photo_file_id)
        await message.reply(messages.message_set.format(action))
    elif action in ("havdalah", "הבדלה"):
        await Chats.update(chat_id=message.chat.id, havdalah_message=text, havdalah_message_img=photo_file_id)
        await message.reply(messages.message_set.format(action))
    elif action in ("holiday", "חג"):
        await Chats.update(chat_id=message.chat.id, holiday_message=text, holiday_message_img=photo_file_id)
        await message.reply(messages.message_set.format(action))
    else:
        await message.reply(messages.available_commands)


@is_admin_message()
@with_language
async def register_group_handler(_, message: Message, language: str):
    chat_id = message.chat.id
    await Chats.update(chat_id=chat_id, register=True)
    await message.reply(Messages(language=language).register_group.format(chat_id))


@is_admin_message()
@with_language
async def unregister_group_handler(_, message: Message, language: str):
    chat_id = message.chat.id
    await Chats.update(chat_id=chat_id, register=False)
    await message.reply(Messages(language=language).unregister_group.format(chat_id))


commands_handlers = [
    MessageHandler(start_handler, filters.command("start") & filters.private),
    MessageHandler(help_handler, filters.command("help") & filters.private),
    MessageHandler(change_language_handler, filters.command("lang") & (filters.private | filters.group)),
    MessageHandler(set_messages_handler, filters.command("set") & filters.group),
    MessageHandler(register_group_handler, filters.command("register") & filters.group),
    MessageHandler(unregister_group_handler, filters.command("unregister") & filters.group),
]
