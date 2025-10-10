from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tools.enums import Messages
from database import BotSettings


def select_language_buttons():
    messages = Messages()
    buttons = []
    row = []

    for i, lang in enumerate(messages.languages(), start=1):
        language_name = messages.languages_names()[i-1]
        row.append(InlineKeyboardButton(
            language_name,
            callback_data=f"lang:{lang}"
        ))
        if i % 2 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)


def buttons_builder(name, data):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(name, callback_data=data)
            ]
        ]
    )


def bot_settings_buttons(bot_settings: BotSettings, language: str):
    messages = Messages(language=language)
    buttons = []
    row = []
    # Define button configurations
    can_join_group = "✅" if bot_settings.can_join_group else "❌"
    can_join_channel = "✅" if bot_settings.can_join_channel else "❌"

    config_buttons = [
        (messages.statistics_button, "bot:statistics"),
        (messages.can_join_group_button.format(can_join_group), "bot:can_join_group"),
        (messages.can_join_channel_button.format(can_join_channel), "bot:can_join_channel"),
        (messages.export_users_button, "bot:users"),
        (messages.export_chats_button, "bot:chats")
    ]

    for button_name, callback_data in config_buttons:
        row.append(InlineKeyboardButton(button_name, callback_data=callback_data))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)
