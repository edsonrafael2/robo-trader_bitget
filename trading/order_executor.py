from config.settings import SIMULATION_MODE, TRADE_MODE, TRADE_PERCENT
import math
import requests
import os
import time
import hmac
import base64
import hashlib
import json


class OrderExecutor:

    def __init__(self, client, symbol, trade_amount):
        self.client = client
        self.symbol = symbol
        self.trade_amount = trade_amount
        self.simulation = SIMULATION_MODE

        self.api_key = os.getenv("BITGET_KEY")
        self.api_secret = os.getenv("BITGET_SECRET")
        self.passphrase = os.getenv("BITGET_PASSPHRASE")

        self.base_url = "https://api.bitget.com"

        # Bitget simplificado (sem step dinâmico por enquanto)
        self.step_size = 0.000001
        self.min_qty = 0.00001

    # =========================
    # PREÇO
    # =========================
    def get_price(self):

        url = f"{self.base_url}/api/spot/v1/market/ticker"
        params = {"symbol": self.symbol}

        response = requests.get(url, params=params).json()

        return float(response['data']['close'])

    # =========================
    # BALANCE
    # =========================
    def get_balance(self):

        # ⚠️ simplificado (pode ajustar depois com assinatura real)
        return 100  # fallback simulado

    # =========================
    # QUANTIDADE
    # =========================
    def calculate_quantity(self):

        price = self.get_price()

        if TRADE_MODE == "FIXED":
            usdt_value = self.trade_amount

        elif TRADE_MODE == "PERCENT":
            balance = self.get_balance()
            usdt_value = balance * TRADE_PERCENT

        raw_quantity = usdt_value / price

        quantity = self._adjust_quantity(raw_quantity)

        print(f"[DEBUG] Raw: {raw_quantity} | Ajustado: {quantity}")

        if quantity < self.min_qty:
            print(f"[ERRO] Quantidade abaixo do mínimo")
            return None

        return quantity

    # =========================
    # ASSINATURA
    # =========================
    def _sign(self, timestamp, method, request_path, body=""):
        message = str(timestamp) + method + request_path + body
        mac = hmac.new(
            bytes(self.api_secret, encoding='utf-8'),
            bytes(message, encoding='utf-8'),
            digestmod=hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode()

    def _headers(self, method, request_path, body=""):
        timestamp = str(int(time.time() * 1000))

        sign = self._sign(timestamp, method, request_path, body)

        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

    # =========================
    # BUY
    # =========================
    def buy(self):

        quantity = self.calculate_quantity()

        if quantity is None:
            return None

        if self.simulation:
            print(f"[SIMULAÇÃO] COMPRA: {quantity}")
            return

        print(f"Executando COMPRA: {quantity}")

        endpoint = "/api/spot/v1/trade/orders"

        body = json.dumps({
            "symbol": self.symbol,
            "side": "buy",
            "orderType": "market",
            "size": str(quantity)
        })

        headers = self._headers("POST", endpoint, body)

        response = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=body
        )

        return response.json()

    # =========================
    # SELL
    # =========================
    def sell(self):

        quantity = self.calculate_quantity()

        if quantity is None:
            return None

        if self.simulation:
            print(f"[SIMULAÇÃO] VENDA: {quantity}")
            return

        print(f"Executando VENDA: {quantity}")

        endpoint = "/api/spot/v1/trade/orders"

        body = json.dumps({
            "symbol": self.symbol,
            "side": "sell",
            "orderType": "market",
            "size": str(quantity)
        })

        headers = self._headers("POST", endpoint, body)

        response = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=body
        )

        return response.json()

    # =========================
    # AJUSTE
    # =========================
    def _adjust_quantity(self, quantity):
        adjusted = math.floor(quantity / self.step_size) * self.step_size
        return round(adjusted, 6)