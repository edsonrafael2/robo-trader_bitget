from market.market_data import MarketData

market = MarketData()

price = market.get_price("BTCUSDT")

print("Preço atual:", price)

candles = market.get_klines("BTCUSDT")

print("Primeiro candle:", candles[0])