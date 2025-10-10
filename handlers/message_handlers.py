from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.enums import MessageServiceType
from database import Chats


async def service_message_handler(client: Client, message: Message):
    if message.service == MessageServiceType.NEW_CHAT_TITLE:
        chat_id = message.chat.id
        new_title = message.new_chat_title
        chat_type = message.chat.type.value
        Chats.update(chat_id=chat_id,
                     chat_type=chat_type,
                     chat_title=new_title)


message_handlers = [MessageHandler(service_message_handler, filters.service)]
