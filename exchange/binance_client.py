from binance.client import Client
import os


class BinanceClient:

    def __init__(self):

        api_key = os.getenv("BINANCE_KEY")
        api_secret = os.getenv("BINANCE_SECRET")

        self.client = Client(api_key, api_secret)

        # # (sincroniza com servidor Binance)
        # self.client.API_URL = 'https://api.binance.com'
        # self.client.get_server_time()

        

    def get_price(self, symbol):

        ticker = self.client.get_symbol_ticker(symbol=symbol)

        return float(ticker["price"])