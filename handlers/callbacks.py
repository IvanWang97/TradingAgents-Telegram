"""
Callback handlers for button clicks.
"""
import asyncio
import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes
import markdown

from storage import UserConfigStorage
from analysis import run_trading_analysis, TRADINGAGENTS_AVAILABLE
from utils import publish_to_telegraph, format_analysis_result_markdown, format_short_message

logger = logging.getLogger(__name__)

user_config_storage = UserConfigStorage()


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data and query.data.startswith("provider:"):
        # Handle provider selection
        provider = query.data.split(":", 1)[1]

        if user_config_storage.set_llm_provider(user_id, provider):
            await query.edit_message_text(
                f"LLM provider set to `{provider}` successfully!",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                f"Failed to set provider to `{provider}`.",
                parse_mode="Markdown"
            )

    elif query.data and query.data.startswith("info:"):
        # Handle ticker analysis
        ticker = query.data.split(":", 1)[1]

        # Send initial message
        await query.edit_message_text(f"Analyzing {ticker}... Please wait.")

        if not TRADINGAGENTS_AVAILABLE:
            await query.edit_message_text(
                "TradingAgents module not available.\n\n"
                "Please install the tradingagents package."
            )
            return

        try:
            # Run TradingAgentsGraph in a thread pool since it's blocking
            final_state, signal = await asyncio.to_thread(
                run_trading_analysis,
                ticker,
                user_id,
                user_config_storage
            )

            if final_state is None:
                await query.edit_message_text(
                    "Analysis failed. TradingAgents module not available."
                )
                return

            # Format as Markdown
            markdown_content = format_analysis_result_markdown(ticker, final_state, signal)
            print(markdown_content)  # Debug print
            # Convert Markdown to HTML
            html_content = markdown.markdown(markdown_content)
            print(html_content)  # Debug print
            # Publish to Telegraph
            telegraph_url = await publish_to_telegraph(f"{ticker} Analysis", html_content)

            # Send short message with Telegraph link
            message = format_short_message(ticker, signal, telegraph_url)
            await query.edit_message_text(message, parse_mode="MarkdownV2")

        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")
            traceback.print_exc()
            await query.edit_message_text(
                f"Error analyzing {ticker}.\n\n"
                f"Details: {str(e)[:200]}"
            )
