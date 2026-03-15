"""
Utility functions for the bot.
Message formatting and sending.
"""
import logging
from telegraph import Telegraph

logger = logging.getLogger(__name__)

# Initialize Telegraph client (using anonymous account)
telegraph = Telegraph()


async def publish_to_telegraph(title: str, content: str) -> str:
    """Publish content to Telegraph and return URL."""
    try:
        page = telegraph.create_page(
            title=title,
            html_content=content,
            author_name="TradingAgents Bot"
        )
        return f"https://telegra.ph/{page['path']}"
    except Exception as e:
        logger.error(f"Failed to publish to Telegraph: {e}")
        return None


async def send_long_message(query, message: str, parse_mode: str = None):
    """Send a long message in chunks to avoid Telegram's 4096 character limit."""
    MAX_LENGTH = 4096

    if len(message) <= MAX_LENGTH:
        await query.edit_message_text(message, parse_mode=parse_mode)
        return

    # Split message into chunks
    chunks = []
    for i in range(0, len(message), MAX_LENGTH):
        chunk = message[i:i + MAX_LENGTH]
        chunks.append(chunk)

    # Send first chunk (edit the original message)
    if parse_mode:
        await query.edit_message_text(chunks[0], parse_mode=parse_mode)
    else:
        await query.edit_message_text(chunks[0])

    # Send remaining chunks as new messages
    for chunk in chunks[1:]:
        await query.message.reply_text(chunk, parse_mode=parse_mode)


def format_analysis_result_markdown(ticker: str, final_state: dict, signal: str) -> str:
    """Format analysis result as Markdown."""
    decision = final_state.get("final_trade_decision", "N/A")
    investment_plan = final_state.get("investment_plan", "N/A")
    trader_plan = final_state.get("trader_investment_plan", "N/A")
    market_report = final_state.get("market_report", "N/A")
    sentiment_report = final_state.get("sentiment_report", "N/A")
    news_report = final_state.get("news_report", "N/A")
    fundamentals_report = final_state.get("fundamentals_report", "N/A")

    return (
        f"## {ticker} Analysis Result\n\n"
        f"**Decision:** {signal}\n\n"
        f"### Final Trade Decision\n\n{decision}\n\n"
        f"### Investment Plan\n\n{investment_plan}\n\n"
        f"### Trader Plan\n\n{trader_plan}\n\n"
        f"### Market Report\n\n{market_report}\n\n"
        f"### Sentiment Report\n\n{sentiment_report}\n\n"
        f"### News Report\n\n{news_report}\n\n"
        f"### Fundamentals Report\n\n{fundamentals_report}\n\n"
    )


def format_short_message(ticker: str, signal: str, telegraph_url: str = None) -> str:
    """Format short message for Telegram with Telegraph link."""
    message = (
        f"*{ticker} Analysis Result*\n\n"
        f"📊 **Decision**: `{signal}`\n\n"
    )
    if telegraph_url:
        message += f"📄 [View Full Report]({telegraph_url})"
    return message
