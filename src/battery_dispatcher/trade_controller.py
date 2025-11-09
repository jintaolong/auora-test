# Assumptions:
# - there's only one market to watch
from datetime import time
import logging

from battery_dispatcher.trade_strat import SimpleDayNightStrategy, TradeStrategy

logger = logging.getLogger(__name__)

# constants
STRATEGIES = {
    1: SimpleDayNightStrategy,
}


class TradeController:

    def run(self):
        """Run the trade controller in a loop."""
        strategy = self.get_strategy()
        strategy.enter()

    def get_strategy(self) -> TradeStrategy:
        """Retrieve the battery dispatch strategy based on external or internal sources.
        TODO: Implement strategy selection logic
        :return: A class of the selected TradeStrategy
        """
        return STRATEGIES.get(1)()
