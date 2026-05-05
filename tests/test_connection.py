from exchange.binance_client import BinanceClient


client = BinanceClient()

price = client.get_price("BTCUSDT")

print("Preço BTCUSDT:", price)