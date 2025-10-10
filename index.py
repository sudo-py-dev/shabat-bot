import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, idle
from tools.logger import logger
from tools.database import create_tables, BotSettings
from tools.tools import register_handlers
from handlers.command_handlers import commands_handlers
from handlers.callback_handlers import callback_query_handlers
from handlers.join_handlers import join_handlers
from handlers.message_handlers import message_handlers
from bot_management.bot_settings import bot_handlers
from bot_management.callback_handlers import bot_callback_handlers


load_dotenv()


api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
token = os.getenv("BOT_TOKEN")
bot_client_name = os.getenv("BOT_CLIENT_NAME")
bot_owner_id = os.getenv("BOT_OWNER_ID")

if not api_id or not api_hash or not token or not bot_client_name or not bot_owner_id:
    raise ValueError("API_ID, API_HASH, BOT_TOKEN, BOT_CLIENT_NAME, and BOT_OWNER_ID must be set in the environment variables")

app = Client(bot_client_name, api_id=api_id, api_hash=api_hash, bot_token=token, skip_updates=False)


register_handlers(
    app,
    commands_handlers,
    callback_query_handlers,
    bot_handlers,
    bot_callback_handlers,
    join_handlers,
    message_handlers
    # add list of handler see example https://github.com/sudo-py-dev/telegram-bot-template/blob/main/handlers/join_handlers.py#L64
)


async def main():
    try:
        # Initialize database first
        await create_tables()

        await app.start()
        me = await app.get_me()
        logger.info(f"Bot https://t.me/{me.username} is now running!")
        
        # Get bot settings
        bot_settings = await BotSettings.get_settings()
        OWNER_ID = int(os.getenv("BOT_OWNER_ID"))
        logger.success("Bot settings initialized successfully")
        if bot_settings.owner_id is None or bot_settings.owner_id != OWNER_ID:
            await BotSettings.update_settings(owner_id=OWNER_ID)
            name = await app.get_chat(OWNER_ID)
            logger.success(f"Bot owner ID updated and the new owner is {OWNER_ID} {name.full_name} successfully")


        await idle()
    except asyncio.CancelledError:
        logger.success("Bot is shutting down...")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        if app.is_connected:
            await app.stop()
            logger.success("Bot stopped successfully")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
