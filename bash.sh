#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if .env file exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Do you want to overwrite it? [y/N]${NC}"
    read -r OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Operation cancelled.${NC}"
        exit 0
    fi
    cp .env ".env.bak.$(date +%Y%m%d%H%M%S)"
    echo -e "${YELLOW}Backup of existing .env file created.${NC}"
fi

# Function to get input with default value
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    
    if [ -n "$default" ]; then
        read -p "$prompt [$default]: " value
        echo "${value:-$default}"
    else
        read -p "$prompt: " value
        echo "$value"
    fi
}

echo -e "\n${GREEN}🚀 Setting up Shabbat Bot environment${NC}\n"

# Get Telegram Bot Configuration
echo -e "${YELLOW}📱 Telegram Bot Configuration:${NC}"
BOT_TOKEN=$(prompt_with_default "  Enter your Telegram Bot Token" "")
API_ID=$(prompt_with_default "  Enter your Telegram API ID" "")
API_HASH=$(prompt_with_default "  Enter your Telegram API Hash" "")
BOT_CLIENT_NAME=$(prompt_with_default "  Enter Bot Client Name (for session)" "shabat_bot")
BOT_OWNER_ID=$(prompt_with_default "  Enter Bot Owner's Telegram ID" "")

# Database Configuration
echo -e "\n${YELLOW}💾 Database Configuration:${NC}"
DATABASE_URL=$(prompt_with_default "  Enter Database URL" "sqlite+aiosqlite:///${BOT_CLIENT_NAME}.sqlite")

# Optional Settings
echo -e "\n${YELLOW}⚙️  Optional Settings:${NC}"
BOT_LANGUAGE=$(prompt_with_default "  Bot Language (he/en/fr)" "he")
BEFORE_SHABAT=$(prompt_with_default "  Minutes before Shabbat to send notifications" "40")
LOG_LEVEL=$(prompt_with_default "  Logging Level (DEBUG/INFO/WARNING/ERROR/CRITICAL)" "INFO")
LOG_FILE=$(prompt_with_default "  Log file path" "bot.log")
SKIP_UPDATES=$(prompt_with_default "  Skip updates on startup? (true/false)" "false")

# Create .env file
echo -e "\n${GREEN}📝 Creating .env file...${NC}"
cat > .env << EOF
# Telegram Bot Configuration
BOT_TOKEN=${BOT_TOKEN}
API_HASH=${API_HASH}
API_ID=${API_ID}
BOT_CLIENT_NAME=${BOT_CLIENT_NAME}
BOT_OWNER_ID=${BOT_OWNER_ID}

# Database configuration
DATABASE_URL=${DATABASE_URL}

# Logging configuration
LOG_LEVEL=${LOG_LEVEL}
LOG_FILE=${LOG_FILE}

# Bot Language
BOT_LANGUAGE=${BOT_LANGUAGE}

# Before Shabbat notification (in minutes)
BEFORE_SHABAT=${BEFORE_SHABAT}

# Skip updates
SKIP_UPDATES=${SKIP_UPDATES}
EOF

echo -e "\n${GREEN}✅ .env file has been created successfully!${NC}"
echo -e "You can now start the bot using: ${YELLOW}./run.sh${NC}"

# Make run.sh executable if it exists
if [ -f "run.sh" ]; then
    chmod +x run.sh
fi

# Make this script executable
chmod +x "$0"
