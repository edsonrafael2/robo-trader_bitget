from dotenv import load_dotenv
from config.settings import  SANDBOX, TIMEFRAME, SYMBOL
import os
import ccxt

load_dotenv()


class ExchangeClient:

    def __init__(self):

        self.exchange = ccxt.bitget({
            "apiKey": os.getenv("BITGET_API_KEY"),
            "secret": os.getenv("BITGET_SECRET_KEY"),
            "password": os.getenv("BITGET_PASSPHRASE"),
            "enableRateLimit": True,
        })

        if SANDBOX:
            self.exchange.set_sandbox_mode(True)

        self.exchange.load_markets()