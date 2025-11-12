from abc import abstractmethod
from datetime import datetime
from datetime import time as datetime_time
import logging
import time
from typing import Tuple

from battery_dispatcher.price_models import MarketOnePriceModel

logger = logging.getLogger(__name__)

    
class TradeStrategy:
    _STRATEGY_ID = 0
    _STRATEGY_NAME = "base_strategy"
    
    @abstractmethod
    def _signal_single_trade(self) -> Tuple[str, float]:
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
    _PEAK_START = datetime_time(16, 0)  # 4:00 PM
    _PEAK_END = datetime_time(20, 0)    # 8:00 PM

    def _signal_single_trade(self) -> Tuple[str, float]:
        """A simple strategy that buys during the day and sells at night.

        Returns:
            A tuple containing the action ('buy', 'sell', 'hold') and the amount.
        """
        now = datetime.now()
        market_model = MarketOnePriceModel()
        current_price = market_model.get_current_price()
        is_peak = self._is_now_peak(now)
        mean = 0
        if is_peak:
            mean = market_model.get_daily_mean(
                # date_start=None,
                # date_end=None,
                minute_start=self._PEAK_START.hour * 60 + self._PEAK_START.minute,
                minute_end=self._PEAK_END.hour * 60 + self._PEAK_END.minute
            )
        else:
            mean = market_model.get_daily_mean(
                minute_start=0,
                minute_end=self._PEAK_START.hour * 60 + self._PEAK_START.minute
            )
            mean_2 = market_model.get_daily_mean(
                minute_start=self._PEAK_END.hour * 60 + self._PEAK_END.minute,
                minute_end=1439
            )
            mean = (mean + mean_2) / 2  # average off-peak mean
        print(
            f"Time now is {now}, the {'peak' if is_peak else 'off-peak'} average price is {mean}"
        )
        print(f"current price: {current_price}")
        if is_peak:
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
            trade_type, trade_amount = self._signal_single_trade()
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

    def _is_now_peak(self, now: datetime) -> bool:
        """Determine if the current time is within peak hours.

        :param now: The current datetime.
        :return: True if within peak hours, False otherwise.
        """
        # TODO: better way to determine peak time
        return now.hour >= self._PEAK_START.hour and now.hour < self._PEAK_END.hour
