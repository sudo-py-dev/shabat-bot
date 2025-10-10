from pyrogram.types import CallbackQuery
from database import Users
from tools.enums import Messages
from pyrogram.handlers import CallbackQueryHandler
from pyrogram import filters


async def select_language_handler(_, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = callback_query.data.split(":")[1]
    if language not in Messages().languages():
        supported_langs = ", ".join(Messages().languages())
        await callback_query.answer(Messages(language="en").language_not_supported.format(language, supported_langs))
        return

    if not (await Users.get(user_id=user_id)):
        full_name = callback_query.from_user.full_name
        username = callback_query.from_user.username
        await Users.create(user_id=user_id, full_name=full_name, username=username, language=language)
    else:
        await Users.update(user_id=user_id, language=language)

    messages = Messages(language=language)
    language_name = messages.messages[language]['language']
    await callback_query.edit_message_text(messages.language_set.format(language_name))


# Add more callback query handlers here


callback_query_handlers = [
    CallbackQueryHandler(select_language_handler, filters.regex(r"lang:(\w{2})"))
]
