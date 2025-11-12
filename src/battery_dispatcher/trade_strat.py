from abc import abstractmethod
from datetime import datetime, time
import logging
import time
from typing import Tuple

from battery_dispatcher.price_models import MarketOnePriceModel

logger = logging.getLogger(__name__)

    
class TradeStrategy:
    _STRATEGY_ID = 0
    _STRATEGY_NAME = "base_strategy"
    
    @abstractmethod
    def signal_single_trade(self) -> Tuple[str, float]:
        """Decide whether to buy, sell, or hold based on the strategy.
        
        Returns:
            A tuple containing the action ('buy', 'sell', 'hold') and the amount.
        """
        raise NotImplementedError
    
    @abstractmethod
    def enter(self):
        """Strategy event loop to observe market conditions and make trade decisions."""
        raise NotImplementedError

    @abstractmethod
    def _exit(self):
        """Exit the strategy and perform any necessary cleanup."""
        raise NotImplementedError
    
    @abstractmethod
    def _on_hold(self):
        """Handle the hold action in the strategy."""
        raise NotImplementedError


class SimpleDayNightStrategy(TradeStrategy):
    _STRATEGY_ID = 1
    _STRATEGY_NAME = "simple_day_night"

    def signal_single_trade(self) -> Tuple[str, float]:
        """A simple strategy that buys during the day and sells at night.

        Returns:
            A tuple containing the action ('buy', 'sell', 'hold') and the amount.
        """
        now = datetime.now()
        market_model = MarketOnePriceModel()
        current_price = market_model.get_current_price()
        is_peak, start, end = (False, 0, 720) if now.hour < 12 else (True, 720, 1439)
        mean = market_model.get_daily_mean(
            # sampling_start_date=None,
            # sampling_end_date=None,
            start_minute=start,
            end_minute=end
        )
        morning_or_evening = "evening" if is_peak else "morning"
        print(
            f"Good {morning_or_evening}, it is {'peak' if is_peak else 'off-peak'}, the {morning_or_evening} mean price is {mean}"
        )
        if is_peak:
            print(f"current price: {current_price}")
            if current_price > mean * 1.05:
                return ("sell", 1.0)  # Sell 1 unit
            else:
                return ("hold", 0.0)  # Hold
        else:
            if current_price < mean * 0.95:
                return ("buy", 1.0)  # Buy 1 unit
            else:
                return ("hold", 0.0)  # Hold

    def enter(self):
        """Strategy event loop to observe market conditions and make trade decisions."""
        while not self._exit():
            trade_type, trade_amount = self.signal_single_trade()
            print(f"Decided to {trade_type} {trade_amount} units.")
            # Observe market conditions
            self._on_hold()  # Sleep for the duration of one market unit

    def _exit(self) -> bool:
        """Decide whether to exit the strategy or not.

        :return: A boolean indicating exit signal.
        """
        to_exit = False
        # event-driven approach
        # to_exit = external_signal_to_exit() 
        return to_exit  # Placeholder: implement exit logic as needed
    
    def _on_hold(self):
        """Handle the hold action in the strategy."""
        time.sleep(2)  # Sleep for two seconds (for testing purposes)
        # event driven approach
        # while external_signal_to_continue():
        #     time.sleep(60)  # Sleep for a minute before checking again
