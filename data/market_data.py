class MarketData:

    def __init__(self, client, symbol, timeframe):
        self.client = client
        self.symbol = symbol
        self.timeframe = timeframe

    def get_candles(self, limit=50):

        candles = self.client.get_klines(
            symbol=self.symbol,
            interval=self.timeframe,
            limit=limit
        )

        return candles