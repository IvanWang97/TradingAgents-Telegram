"""
Utility functions for the bot.
Message formatting and sending.
"""
import logging
from bs4 import BeautifulSoup
from telegraph import Telegraph

logger = logging.getLogger(__name__)

# Initialize Telegraph client (using anonymous account)
telegraph = Telegraph()


def sanitize_html_for_telegraph(html: str) -> str:
    """Convert HTML to Telegraph-compatible format."""
    soup = BeautifulSoup(html, "html.parser")

    # Map unsupported HTML tags to Telegraph-supported ones
    tag_map = {
        "h1": "h3",
        "h2": "h3",
        "h3": "h4",
        "h4": "h4",
        "h5": "h4",
        "h6": "h4",
    }

    for element in soup.find_all(list(tag_map.keys())):
        element.name = tag_map[element.name]

    return str(soup)


async def publish_to_telegraph(title: str, content: str) -> str:
    """Publish content to Telegraph and return URL."""
    try:
        cleaned_html = sanitize_html_for_telegraph(content)
        page = telegraph.create_page(
            title=title,
            html_content=cleaned_html,
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
