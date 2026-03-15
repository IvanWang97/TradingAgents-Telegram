# TradingAgents Telegram Bot

Telegram bot for managing stock watchlists.

## Features

- `/add <ticker>` - Add a stock to watchlist (e.g., `/add NVDA`)
- `/del <ticker>` - Remove a stock from watchlist (e.g., `/del NVDA`)
- `/watch` or `/list` - List all watchlisted stocks with clickable buttons
- `/start` - Welcome message
- `/help` - Show help

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Telegram bot token:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## Getting a Bot Token

1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow the instructions
3. Copy the token and set it as environment variable

## Data Storage

Watchlists are stored in `data/watchlist.json` in the telegram_bot directory.
