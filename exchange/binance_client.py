import time
#from binance.client import Client
import os


# class BinanceClient:

#     def __init__(self):

#         api_key = os.getenv("BINANCE_KEY")
#         api_secret = os.getenv("BINANCE_SECRET")

#         self.client = Client(api_key, api_secret)

#         # Ajuste automático de horário
#         #server_time = self.client.get_server_time()
#         #system_time = int(time.time() * 1000)
#         #offset = server_time['serverTime'] - system_time
#         #self.client.timestamp_offset = offset
#         #print(f"[TIME SYNC] Offset Binance: {offset} ms")


#     def get_price(self, symbol):

#         ticker = self.client.get_symbol_ticker(symbol=symbol)

#         return float(ticker["price"])
