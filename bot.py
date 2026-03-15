"""
Telegram Bot for TradingAgents - Watchlist Management.
Main entry point for the bot application.
"""
import sys
import logging
import os
from pathlib import Path


def setup_tradingagents_path() -> bool:
    """
    Setup TradingAgents path in sys.path.

    Priority order:
    1. TRADINGAGENTS_PATH env var
    2. ../TradingAgents (sibling directory)
    3. Assume installed as package

    Returns:
        True if TradingAgents was found in sys.path
    """
    # 1. Environment variable
    env_path = os.getenv("TRADINGAGENTS_PATH")
    if env_path and Path(env_path).exists():
        sys.path.insert(0, env_path)
        logging.info(f"Using TRADINGAGENTS_PATH: {env_path}")
        return True

    # 2. Sibling directory (../TradingAgents)
    current_dir = Path(__file__).parent
    # TradingAgents is at ../TradingAgents
    sibling_tradingagents_path = current_dir.parent / "TradingAgents"
    if sibling_tradingagents_path.exists():
        # Check if tradingagents module exists inside
        if (sibling_tradingagents_path / "tradingagents").exists():
            # Add sibling TradingAgents directory to path
            sys.path.insert(0, str(sibling_tradingagents_path))
            logging.info(f"Using sibling TradingAgents: {sibling_tradingagents_path}")
            return True

    # 3. Assume installed as package
    logging.info("Assuming TradingAgents is installed as a package")
    return True


# Setup TradingAgents path
setup_tradingagents_path()

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from config import Config
from handlers import (
    start,
    help_cmd,
    add_ticker,
    del_ticker,
    list_watchlist,
    config_cmd,
    button_callback,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    if not Config.validate():
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        logger.info("Please set TELEGRAM_BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("add", add_ticker))
    application.add_handler(CommandHandler("del", del_ticker))
    application.add_handler(CommandHandler("watch", list_watchlist))
    application.add_handler(CommandHandler("list", list_watchlist))
    application.add_handler(CommandHandler("config", config_cmd))

    # Register callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
