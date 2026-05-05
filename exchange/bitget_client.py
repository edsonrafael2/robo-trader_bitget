import requests
import time
import os
import hmac
import base64
import hashlib


class BitgetClient:

    def __init__(self):
        self.api_key = os.getenv("BITGET_KEY")
        self.api_secret = os.getenv("BITGET_SECRET")
        self.passphrase = os.getenv("BITGET_PASSPHRASE")

        self.base_url = "https://api.bitget.com"

    def get_price(self, symbol):

        url = f"{self.base_url}/api/spot/v1/market/ticker"
        params = {"symbol": symbol}

        response = requests.get(url, params=params).json()

        return float(response['data']['close'])