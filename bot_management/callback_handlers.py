import json
import tempfile
from datetime import datetime
from pathlib import Path
from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import CallbackQuery
from tools.database import Users, Chats, BotSettings
from tools.tools import with_language, owner_only
from tools.inline_keyboards import bot_settings_buttons, buttons_builder
from tools.logger import logger
from tools.enums import Messages
from typing import Dict, Any, List


def _serialize_value(value):
    """Recursively serialize values to be JSON-compatible."""
    from datetime import datetime
    
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return [_serialize_value(item) for item in value]
    return value


@owner_only
@with_language
async def handle_bot_callbacks(_, query: CallbackQuery, language: str):
    """Handle all bot-related callback queries.
    
    Args:
        _: Unused client parameter
        query: The callback query object
        language: User's language code
    """
    messages = Messages(language=language)
    data = query.data.split(":")
    
    if len(data) < 2:
        return
    
    action = data[1].strip()
    
    # Handle statistics
    if action == "statistics":
        users = await Users().count()
        active_users = await Users().count_by(is_active=True)
        chats = await Chats().count()
        active_chats = await Chats().count_by(is_active=True)
        
        back_button = buttons_builder(messages.back_button, "bot:back")
        
        text = messages.statistics.format(users, active_users, chats, active_chats)
        await query.edit_message_text(
            text,
            reply_markup=back_button
        )

    elif action in ("users", "chats"):
        await _handle_export(query, messages, action)

    elif action in ("can_join_group", "can_join_channel", "back"):
        if action != "back":
            await BotSettings.switch_settings(action)
        await query.edit_message_text(
            messages.bot_settings,
            reply_markup=bot_settings_buttons(await BotSettings.get_settings(), language)
        )


async def _handle_export(query: CallbackQuery, messages: Messages, data_type: str) -> None:
    """Export all users or chats as JSON and send as a document."""
    model = Users() if data_type == "users" else Chats()
    items = await model.get_all()
    if not items:
        await query.answer(messages.no_data_to_export, show_alert=True)
        return

    await query.answer(messages.exporting_data)
    data = _serialize_value(items)
    filename = f"{data_type}_export_{datetime.now():%Y%m%d_%H%M%S}.json"

    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", suffix=".json", delete=True) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.seek(0)
        await query.message.reply_document(
            document=tmp.name,
            file_name=filename,
            caption=messages.export_success.format(data_type),
        )



bot_callback_handlers = [
    CallbackQueryHandler(
        handle_bot_callbacks,
        filters.regex(r"^bot:(\w+)$")
    )
]
