
import requests


class MarketData:

    def __init__(self):
        self.base_url = "https://api.bitget.com"

    def get_price(self, symbol):

        url = f"{self.base_url}/api/spot/v1/market/ticker"
        params = {"symbol": symbol}

        response = requests.get(url, params=params).json()

        return float(response['data']['close'])

    def get_klines(self, symbol, interval="1min", limit=50):

        url = f"{self.base_url}/api/spot/v1/market/candles"

        params = {
            "symbol": symbol,
            "period": interval,
            "limit": limit
        }

        response = requests.get(url, params=params).json()

        return response['data']




# from exchange.binance_client import BinanceClient


# class MarketData:

#     def __init__(self):

#         self.binance = BinanceClient()
#         self.client = self.binance.client

#     def get_price(self, symbol):

#         return self.binance.get_price(symbol)

#     def get_klines(self, symbol, interval="1m", limit=50):

#         candles = self.client.get_klines(
#             symbol=symbol,
#             interval=interval,
#             limit=limit
#         )

#         return candles