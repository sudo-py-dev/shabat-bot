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

# Check for .env and handle overwrite
if [ -f ".env" ]; then
    if [ -f ".skip_env" ]; then
        echo -e "${YELLOW}ℹ️  Using existing .env file (auto-skip enabled)${NC}"
    else
        echo -e "${YELLOW}⚠️  .env file already exists.${NC}"
        read -p "Do you want to overwrite it? [y/N] " -n 1 -r OVERWRITE
        echo
        
        if [[ $OVERWRITE =~ ^[Yy]$ ]]; then
            mkdir -p .backups
            cp .env ".backups/.env.bak.$(date +%Y%m%d%H%M%S)"
            echo -e "${YELLOW}✓ Backup of existing .env file created in .backups/ directory.${NC}"
            
            # Ensure .backups directory is in .gitignore
            if ! grep -q "^.backups/" .gitignore 2>/dev/null; then
                echo -e "\n# Backups directory" >> .gitignore
                echo ".backups/" >> .gitignore
                echo -e "${YELLOW}✓ Added .backups/ to .gitignore${NC}"
            fi
            # Continue with setup after backup
            RUN_SETUP=true
        else
            read -p "Skip this warning in the future? [y/N] " -n 1 -r SKIP_FUTURE
            echo
            if [[ $SKIP_FUTURE =~ ^[Yy]$ ]]; then
                touch .skip_env
                echo -e "${YELLOW}✓ Will use existing .env file without asking in the future.${NC}"
            fi
            echo -e "${YELLOW}Using existing .env file.${NC}"
            RUN_SETUP=false
        fi
    fi
else
    RUN_SETUP=true
fi

if [ "$RUN_SETUP" = true ]; then

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
echo -e "\n${YELLOW}📱 Telegram Bot Configuration:${NC}"
echo -e "${YELLOW}  🔗 Get your API credentials from: https://my.telegram.org/auth${NC}"
echo -e "${YELLOW}  🤖 Create a new bot and get token from: https://t.me/BotFather${NC}\n"

BOT_TOKEN=$(prompt_with_default "  Enter your Telegram Bot Token" "")
API_ID=$(prompt_with_default "  Enter your Telegram API ID" "")
API_HASH=$(prompt_with_default "  Enter your Telegram API Hash" "")
BOT_CLIENT_NAME=$(prompt_with_default "  Enter Bot Client Name (for session)" "shabat_bot")
BOT_OWNER_ID=$(prompt_with_default "  Enter Bot Owner's Telegram ID (get it from @userinfobot on Telegram)" "")

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

fi  # This closes the if [ "$RUN_SETUP" = true ] block

# Ask if user wants to run the bot now
read -p "Do you want to start the bot now? [Y/n] " -n 1 -r START_BOT
echo
if [[ $START_BOT =~ ^[Yy]$ ]] || [ -z "$START_BOT" ]; then
    echo -e "\n${GREEN}🚀 Starting the bot...${NC}"
    python3 index.py
else
    echo -e "\nYou can start the bot later by running: ${YELLOW}python3 index.py${NC}"
fi

# Make this script executable
chmod +x "$0"
