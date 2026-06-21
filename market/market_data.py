
# from exchange.binance_client import BinanceClient


# class MarketData:

#     def __init__(self, client, symbol, timeframe):

#         self.client = client
#         self.symbol = symbol
#         self.timeframe = timeframe

#     def get_candles(self, limit=50):

#         candles = self.client.get_klines(
#             symbol=self.symbol,
#             interval=self.timeframe,
#             limit=limit
#         )

#         return candles

#===============================================================================================


# from exchange.binance_client import BinanceClient


# class MarketData:

#     def __init__(self):

#         self.client = BinanceClient()

#     def get_price(self, symbol):

#         return self.client.get_price(symbol)

#     def get_klines(self, symbol, interval="1m", limit=50):

#         candles = self.client.client.get_klines(
#             symbol=symbol,
#             interval=interval,
#             limit=limit
#         )

#         return candles


from exchange.binance_client import BinanceClient


class MarketData:

    def __init__(self):

        self.binance = BinanceClient()
        self.client = self.binance.client

    def get_price(self, symbol):

        return self.binance.get_price(symbol)

    def get_klines(self, symbol, interval="1m", limit=50):

        candles = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )

        return candles