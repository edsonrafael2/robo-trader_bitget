# from exchange.binance_client import BinanceClient


# client = BinanceClient()

# price = client.get_price("BTCUSDT")

# print("Preço BTCUSDT:", price)


# import ccxt
# from dotenv import load_dotenv
# import os

# load_dotenv()

# exchange = ccxt.bitget({
#     "apiKey": os.getenv("BITGET_API_KEY"),
#     "secret": os.getenv("BITGET_SECRET"),
#     "password": os.getenv("BITGET_PASSPHRASE"),
# })

# print(exchange.fetch_ticker("BTC/USDT"))



import ccxt
from dotenv import load_dotenv
import os

load_dotenv()

#print("API:", os.getenv("BITGET_API_KEY"))
#print("SECRET:", os.getenv("BITGET_SECRET_KEY"))
#print("PASS:", os.getenv("BITGET_PASSPHRASE"))

exchange = ccxt.bitget({
    "apiKey": os.getenv("BITGET_API_KEY"),
    "secret": os.getenv("BITGET_SECRET_KEY"),
    "password": os.getenv("BITGET_PASSPHRASE"),
})

balance = exchange.fetch_balance()

print(balance["USDT"])