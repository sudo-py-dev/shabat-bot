# 🤖 Telegram Bot Template

A modern, feature-rich Telegram bot template built with Pyrogram and Python. This template provides a solid foundation for building Telegram bots with multi-language support, database integration, admin management, advanced control panel, and more.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PyroTGFork](https://img.shields.io/badge/PyroTGFork-2.0+-blue)](https://pypi.org/project/pyrotgfork/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue)](https://t.me/termux_il)

## 👑 Admin System

- **Admin Commands**:
  - `/settings` - Bot settings panel (owner only)
  - `/stats` - View bot statistics
  - `/broadcast` - Send messages to all users (owner only)
  - `/ban` - Ban users from using the bot
  - `/unban` - Unban users

## 🛠️ Bot Management

- **Owner Setup**:
  - First-time setup wizard for bot owner
  - Interactive console for configuration
  - Welcome message on successful setup
- **Settings**:
  - Toggle bot features (group join, channel join)
  - View statistics and bot status
  - Manage bot permissions

## 📁 Project Structure

```
telegram-bot-template/
├── bot_management/           # Bot administration and owner tools
│   ├── bot_settings.py       # Bot settings command and handlers
│   └── callback_handlers.py  # Callback handlers for admin panel
│   └── setup.py              # Bot setup and initialization utilities
├── handlers/                 # Message and callback handlers
│   ├── callback_handlers.py  # Callback query handlers
│   ├── command_handlers.py   # Command handlers (/start, /help, etc.)
│   └── join_handlers.py       # Group join handlers
├── locales/                  # Localization files
│   └── messages.json         # Multi-language messages
└── tools/                    # Core utilities and services
    ├── database.py           # Database models and operations
    ├── enums.py              # Enums and message management
    ├── inline_keyboards.py   # Inline keyboard generators
    ├── logger.py             # Logging configuration
    └── tools.py              # Utility functions and decorators
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore patterns
├── index.py                 # Main bot entry point
├── requirements.txt         # Python dependencies
└── README.md                # This file

## 🛠️ Usage

### Adding New Commands

1. **Create a handler function** in `handlers/commands.py`:
   ```python
   from tools.tools import with_language
   from tools.enums import Messages

   @with_language
   async def my_command(client, message, language: str):
       await message.reply(Messages(language=language).my_message)
   ```

2. **Register the command** in `commands_handlers` list:
   ```python
   commands_handlers = [
       MessageHandler(my_command, filters.command("mycommand")),
       # ... existing handlers
   ]
   ```

### Adding New Languages

1. **Add messages** to `tools/messages.json`:
   ```json
   {
     "fr": {
       "hello": "Bonjour {}",
       "goodbye": "Au revoir"
     }
   }
   ```

2. **Update language display names** in `handlers/callback_buttons.py`:
   ```python
   language_display_names = {
       "he": "עברית 🇮🇱",
       "en": "English 🇺🇸",
       "fr": "Français 🇫🇷"
   }
   ```

### Database Operations

```python
from database import Users

# Create user
Users.create(user_id=123456789, username="user",full_name="user", language="en", is_active=True)

# Get user
user = Users.get(user_id=123456789)

# Update user
Users.update(user_id=123456789, language="he")
```

## 🌍 Multi-language System

The bot supports multiple languages with a sophisticated message management system:

- **Message Storage**: All messages stored in JSON format
- **Fallback System**: Falls back to English if message not found
- **Dynamic Loading**: Languages loaded from `messages.json` at runtime
- **Easy Extension**: Add new languages by updating JSON file

## 👑 Admin System

Advanced admin permission checking with support for:
- **Granular Permissions**: Check specific admin rights
- **Chat Types**: Works with groups, supergroups, and channels
- **Caching**: Admin lists cached for performance
- **Error Handling**: Graceful handling of invalid chats/permissions

```python
from tools.tools import is_admin_message

@is_admin_message(permission_require="can_restrict_members")
async def admin_only_command(client, message):
    await message.reply("You are an admin!")
```

## 📊 Logging

Comprehensive logging system with:
- **File Rotation**: Automatic log file rotation (5MB max, 3 backups)
- **Multiple Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Console Output**: Real-time console logging
- **Structured Format**: Detailed log messages with timestamps

## 🔧 Advanced Features

### Caching System
- **Persistent Cache**: Data survives bot restarts
- **TTL Support**: Automatic expiration of cached data
- **LRU Eviction**: Automatic cleanup of old entries
- **Thread Safe**: Safe for concurrent access

### Database Models
- **Users**: User management with preferences
- **Chats**: Chat information and settings
- **Extensible**: Easy to add new models

### Error Handling
- **Graceful Degradation**: Bot continues running despite errors
- **User Feedback**: Clear error messages for users
- **Debugging Support**: Detailed error logging

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Report Bugs**
   - Check existing issues to avoid duplicates
   - Provide detailed reproduction steps
   - Include error logs and screenshots if applicable

2. **Suggest Enhancements**
   - Open an issue to discuss your idea
   - Explain why this feature would be valuable
   - Include any relevant examples or references

3. **Submit Code Changes**
   - Fork the repository
   - Create a feature branch: `git checkout -b feature/amazing-feature`
   - Commit your changes: `git commit -m 'Add amazing feature'`
   - Push to the branch: `git push origin feature/amazing-feature`
   - Open a Pull Request with a clear description of changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Special thanks to the following open source projects that made this template possible:

- [Pyrogram](https://docs.pyrogram.org/) - Elegant, modern and asynchronous Telegram MTProto API framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - The Database Toolkit for Python
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Read key-value pairs from a .env file
- [aiosqlite](https://aiosqlite.omnilib.dev/) - Async interface to SQLite
- [loguru](https://github.com/Delgan/loguru) - Python logging made (stupidly) simple

## 🌟 Support

If you find this project useful, please consider giving it a ⭐️ on GitHub!

## 📢 Stay Updated

Follow us for updates and more open-source projects:
- [GitHub](https://github.com/sudo-py-dev)
- [Twitter](https://twitter.com/sudo_py_dev)
- [Telegram Channel](https://t.me/sudo_py_dev)

## 📞 Need Help?

If you have any questions or need assistance:
- Check the [documentation](https://github.com/sudo-py-dev/telegram-bot-template/wiki)
- Open an [issue](https://github.com/sudo-py-dev/telegram-bot-template/issues)
- Join our [Telegram group](https://t.me/sudo_py_dev_chat)