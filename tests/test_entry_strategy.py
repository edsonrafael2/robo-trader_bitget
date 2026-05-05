from market.market_data import MarketData
from strategies.entry_strategy import EntryStrategy

market = MarketData()

candles = market.get_klines("BTCUSDT", "5m", 100)

strategy = EntryStrategy(candles)

signal = strategy.check_entry()

print("Sinal de entrada:", signal)