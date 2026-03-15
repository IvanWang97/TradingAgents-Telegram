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
    content = f"**{ticker} Analysis Result**\n\n**Decision:** {signal}\n\n"
    for key, value in final_state.items():
        title = key.replace('_', ' ').title()
        content += f"\n**{title}**\n{value}\n"
    return content


def format_short_message(ticker: str, signal: str, telegraph_url: str = None) -> str:
    """Format short message for Telegram with Telegraph link."""
    message = (
        f"*{ticker} Analysis Result*\n\n"
        f"📊 **Decision**: `{signal}`\n\n"
    )
    if telegraph_url:
        message += f"📄 [View Full Report]({telegraph_url})"
    return message
