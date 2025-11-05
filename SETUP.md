# Discord & Telegram Member Scraper Setup Guide

This repository contains official API-based scrapers for Discord and Telegram.

## Discord Scraper Setup

### Prerequisites
- Node.js installed (v16 or higher)
- Discord account
- Server where you have permission to add a bot

### Step 1: Install Dependencies
```bash
npm install discord.js
```

### Step 2: Create a Discord Bot
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Give it a name and create
4. Go to "Bot" section in the left sidebar
5. Click "Add Bot"
6. Under "Privileged Gateway Intents", enable:
   - Server Members Intent
   - Presence Intent (optional)
7. Click "Reset Token" and copy your bot token

### Step 3: Invite Bot to Your Server
1. Go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`
3. Select permissions: `Read Messages/View Channels`
4. Copy the generated URL and paste in browser
5. Select your server and authorize

### Step 4: Configure and Run
```bash
# Set environment variables
export DISCORD_BOT_TOKEN="your_bot_token_here"
export DISCORD_SERVER_ID="your_server_id_here"

# Run the scraper
node discord-scraper.js
```

### Output
- `discord_members.json` - Full member data in JSON format
- `discord_members.csv` - Member data in CSV format

---

## Telegram Scraper Setup

### Prerequisites
- Python 3.7 or higher
- Telegram account with phone number

### Step 1: Install Dependencies
```bash
pip install telethon pandas
```

### Step 2: Get Telegram API Credentials
1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Click "API development tools"
4. Create a new application (any name/description)
5. Copy your `api_id` and `api_hash`

### Step 3: Configure and Run
```bash
# Set environment variables
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
export TELEGRAM_PHONE="+1234567890"  # Your phone with country code
export TELEGRAM_CHANNEL="channel_username"  # Without @

# Run the scraper
python telegram-member-scrape.py
```

### First Run
- You will be prompted to enter a verification code sent to your Telegram app
- A session file will be created for future runs (no code needed again)

### Output
- `{channel}_members.json` - Full member data in JSON format
- `{channel}_members.csv` - Member data in CSV format

---

## Important Notes

### Data Collection Ethics
- Only scrape servers/channels you own or have permission to scrape
- Respect user privacy - collected data should not be used for spam or harassment
- Follow Discord and Telegram Terms of Service
- Do not share or sell user data

### Rate Limits
- **Discord**: Handled automatically by discord.js library
- **Telegram**: Built-in 2-second delay between requests
  - If rate limited, the script will wait automatically

### Legal Compliance
- Only collect publicly available information
- Phone numbers are NOT collected (privacy concern)
- Ensure compliance with GDPR, CCPA, and local data protection laws

### Troubleshooting

**Discord "Server not found"**
- Make sure bot is invited to the server
- Check that SERVER_ID is correct (enable Developer Mode in Discord, right-click server, Copy ID)

**Telegram "Admin privileges required"**
- Channel has private member list
- You need to be an admin to access members

**Telegram "FloodWaitError"**
- Telegram is rate limiting you
- Script will wait automatically
- Reduce BATCH_SIZE or increase RATE_LIMIT_DELAY in config

---

## Example Usage

### Discord
```bash
# Quick run with inline config
DISCORD_BOT_TOKEN="MTIzNDU2..." DISCORD_SERVER_ID="987654321" node discord-scraper.js
```

### Telegram
```bash
# Quick run with inline config
TELEGRAM_API_ID="12345" TELEGRAM_API_HASH="abc123..." TELEGRAM_PHONE="+1234567890" TELEGRAM_CHANNEL="python" python telegram-member-scrape.py
```

---

## Data Format

### Discord Output
```json
{
  "username": "user123",
  "display_name": "User Name",
  "id": "123456789",
  "discriminator": "1234",
  "bot": false,
  "joined_at": "2024-01-01T12:00:00.000Z",
  "roles": ["Member", "Verified"],
  "nickname": "Custom Nick",
  "avatar_url": "https://..."
}
```

### Telegram Output
```json
{
  "id": 123456789,
  "username": "user123",
  "first_name": "John",
  "last_name": "Doe",
  "is_bot": false,
  "is_premium": false,
  "scraped_at": "2024-01-01T12:00:00"
}
```
