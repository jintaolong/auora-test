from abc import abstractmethod
import datetime
import os
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Optional, Tuple

file_path = os.path.dirname(__file__)
print(file_path)

class PriceModelBase:

    def __init__(self):
        self._load_model()

    @abstractmethod
    def _load_model(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_current_price(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_daily_mean(self,
                       sampling_start_date: Optional[datetime.date] = None,
                       sampling_end_date: Optional[datetime.date] = None,
                       start_minute: Optional[int] = None, 
                       end_minute: Optional[int] = None) -> float:
        raise NotImplementedError

    @abstractmethod
    def predict_price(self, units_ahead: int) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def update_model(self, new_data: pd.DataFrame):
        raise NotImplementedError


class MarketTwoPriceModel(PriceModelBase):
    _time_unit = 60  # in minutes

    def _load_model(self):
        self._data = pd.read_excel(Path(file_path) / 'data/markets.xlsx', sheet_name=0)

    def get_current_price(self) -> float:
        """Retrieve the current price for Market One."""
        return np.random.rand() * 80 + 0 # yield a number randomly between 0 - 80

    def get_daily_mean(self,
                       date_start: Optional[datetime.datetime] = datetime.datetime.min,
                       date_end: Optional[datetime.datetime] = datetime.datetime.max,
                       minute_start: Optional[int] = 0,
                       minute_end: Optional[int] = 1439) -> float:
        """Calculate the daily mean price with specific constraints for Market One."""
        # add a day minute column to filter by start/end min of each day
        df = self._data.assign(
            day_minute=self._data.apply(
                lambda row: row.iloc[0].hour * 60 + row.iloc[0].minute,
                axis=1
            )
        )
        # Filter by date range if provided
        mask = (df.iloc[:, 0] > date_start) & \
               (df.iloc[:, 0] < date_end) & \
               (df['day_minute'] > minute_start) & \
               (df['day_minute'] < minute_end)
        df = df[mask]
        return df.iloc[:, 1].mean()

    def predict_price(self, units_ahead: int) -> float:
        """Predict the price for Market One a certain number of units ahead."""
        pass

    def update_model(self, new_data: pd.DataFrame):
        """Update the model with new data for Market One."""
        pass
    