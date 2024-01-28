import os
from lumibot.brokers.vanilla import Vanilla
from lumibot.data_sources.vanilla_data import VanillaData
from lumibot.example_strategies.stock_buy_and_hold import BuyAndHold

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

BINANCE_CONFIG = {  # Paper trading!
    # Put your own binance key here:
    "API_KEY": api_key,
    # Put your own binance secret here:
    "API_SECRET": api_secret,
}

def test_initialize_broker_legacy():
    """
    This test to make sure the legacy way of initializing the broker still works.
    """
    broker = Vanilla(BINANCE_CONFIG)
    strategy = BuyAndHold(
        broker=broker,
    )

    # Assert that strategy.broker is the same as broker
    assert strategy.broker == broker

    # Assert that strategy.data_source is AlpacaData object
    assert isinstance(strategy.broker.data_source, VanillaData)
