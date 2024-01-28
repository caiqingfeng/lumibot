import logging
from datetime import datetime

import pytz

from lumibot.entities import Bars
from lumibot.tools.helpers import create_options_symbol, parse_timestep_qty_and_unit

from .data_source import DataSource


class VanillaData(DataSource):
    MIN_TIMESTEP = "minute"
    SOURCE = "Vanilla"
    TIMESTEP_MAPPING = [
        {
            "timestep": "tick",
            "representations": [
                "tick",
            ],
        },
        {
            "timestep": "minute",
            "representations": [
                "minute",
            ],
        },
        {
            "timestep": "day",
            "representations": [
                "daily",
            ],
        },
        {
            "timestep": "week",
            "representations": [
                "weekly",
            ],
        },
        {
            "timestep": "month",
            "representations": [
                "monthly",
            ],
        },
    ]

    def __init__(self, max_workers=20):
        super().__init__(api_key=access_token)
        self.max_workers = min(max_workers, 50)

    def get_historical_prices(
        self, asset, length, timestep="", timeshift=None, quote=None, exchange=None, include_after_hours=True
    ):
        """
        Get bars for a given asset

        Parameters
        ----------
        asset : Asset
            The asset to get the bars for.
        length : int
            The number of bars to get.
        timestep : str
            The timestep to get the bars at. For example, "minute" or "day".
        timeshift : datetime.timedelta
            The amount of time to shift the bars by. For example, if you want the bars from 1 hour ago to now,
            you would set timeshift to 1 hour.
        quote : Asset
            The quote asset to get the bars for.
        exchange : str
            The exchange to get the bars for.
        include_after_hours : bool
            Whether to include after hours data.
        """

        timestep = timestep if timestep else self.MIN_TIMESTEP

        # Parse the timestep
        timestep_qty, timestep_unit = parse_timestep_qty_and_unit(timestep)

        parsed_timestep_unit = self._parse_source_timestep(timestep_unit, reverse=True)

        end_date = datetime.now()

        # Use pytz to get the US/Eastern timezone
        eastern = pytz.timezone("US/Eastern")

        # Convert datetime object to US/Eastern timezone
        end_date = end_date.astimezone(eastern)

        # Calculate the end date
        if timeshift:
            end_date = end_date - timeshift

        # Calculate the start date
        td, _ = self.convert_timestep_str_to_timedelta(timestep)
        start_date = end_date - (td * length)

        try:
            df = []
        except Exception as e:
            logging.error(f"Error getting historical prices for {asset}: {e}")
            return None

        # Convert the dataframe to a Bars object
        bars = Bars(df, self.SOURCE, asset, raw=df, quote=quote)

        return bars

    def get_last_price(self, asset, quote=None, exchange=None):
        """
        This function returns the last price of an asset.
        Parameters
        ----------
        asset
        quote
        exchange

        Returns
        -------
        float
           Price of the asset
        """

        #price = self.tradier.market.get_last_price(asset)
        return price
