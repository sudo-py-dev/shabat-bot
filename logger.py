import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Constants
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'bot.log')
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB per file
BACKUP_COUNT = 5
LOG_LEVEL = logging.INFO

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Set up the logger
logger = logging.getLogger('bot')
logger.setLevel(LOG_LEVEL)

# Prevent adding multiple handlers if the logger is already configured
if not logger.handlers:
    # Create a more detailed formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    try:
        # File handler with rotation
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    except Exception as e:
        print(f"Failed to initialize logging: {e}", file=sys.stderr)
        raise
