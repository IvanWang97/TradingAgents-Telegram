"""
TradingAgentsGraph analysis functions.
"""
import logging
from datetime import date

logger = logging.getLogger(__name__)

# Import TradingAgentsGraph - tradingagents is treated as an external module
TRADINGAGENTS_AVAILABLE = False
TradingAgentsGraph = None
DEFAULT_CONFIG = None

try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph as _TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG as _DEFAULT_CONFIG
    TradingAgentsGraph = _TradingAgentsGraph
    DEFAULT_CONFIG = _DEFAULT_CONFIG
    TRADINGAGENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"TradingAgents not available. Error: {e}")


def run_trading_analysis(ticker: str, user_id: str, user_config_storage):
    """Run TradingAgentsGraph analysis for a ticker.

    Args:
        ticker: Stock ticker symbol
        user_id: User ID for getting user config
        user_config_storage: UserConfigStorage instance

    Returns:
        Tuple of (final_state, signal) or (None, None) if not available
    """
    if not TRADINGAGENTS_AVAILABLE:
        return None, None

    # Get user's LLM provider config, fallback to default
    user_provider = user_config_storage.get_llm_provider(user_id)
    config = DEFAULT_CONFIG.copy()
    if user_provider:
        config["llm_provider"] = user_provider

    ta = TradingAgentsGraph(debug=True, config=config)
    final_state, signal = ta.propagate(company_name=ticker, trade_date=date.today())

    # Log the final_state for debugging
    logger.info(f"Final state for {ticker}: {final_state}")

    return final_state, signal
