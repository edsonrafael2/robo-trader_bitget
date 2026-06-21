from config.settings import SIMULATION_MODE, TRADE_MODE, TRADE_PERCENT # Usado no simulador
import math

class OrderExecutor:

    def __init__(self, client, symbol, trade_amount):
        self.client = client
        self.symbol = symbol
        self.trade_amount = trade_amount
        self.simulation = SIMULATION_MODE # Usado no simulador
        self.step_size, self.min_qty = self._get_lot_size_filters()

    def get_price(self):

        ticker = self.client.get_symbol_ticker(symbol=self.symbol)
        return float(ticker["price"])

    # def calculate_quantity(self):

    #     price = self.get_price()

    #     quantity = self.trade_amount / price

    #     return round(quantity, 6)

    def get_balance(self):
        try:
            # Busca o saldo da carteira Spot para a moeda que você usa para comprar (USDT)
            account_info = self.client.get_asset_balance(asset="USDT")
            return float(account_info['free'])
        except Exception as e:
            print(f"[ERRO] Não foi possível buscar o saldo de USDT: {e}")
            return 0.0

    def calculate_quantity(self):
        price = self.get_price()

        if TRADE_MODE == "FIXED":
            usdt_value = self.trade_amount

        elif TRADE_MODE == "PERCENT":
            balance = self.get_balance()
            usdt_value = balance * TRADE_PERCENT

        if usdt_value < 5:
            print("[ERRO] Saldo insuficiente")
            return None

        raw_quantity = usdt_value / price

        quantity = self._adjust_quantity(raw_quantity)

        print(f"[DEBUG] USDT: {usdt_value:.2f} [DEBUG] Raw: {raw_quantity} | Ajustado: {quantity}")

        if quantity < self.min_qty:
            print(f"[ERRO] Quantidade abaixo do mínimo: {quantity} < {self.min_qty}")
            return None

        return quantity

    def buy(self):

        quantity = self.calculate_quantity()

        if quantity is None:
            return None

        # Condição abaixo usado para a simulação
        if self.simulation:
            print(f"[SIMULAÇÃO] COMPRA: {quantity}")
            return {"status": "simulated_buy", "quantity": quantity}

        print(f"Executando COMPRA: {quantity}")

        order = self.client.order_market_buy(
            symbol=self.symbol,
            quantity=quantity
        )

        return order

 
    def sell(self):
        # 1. Condicional usado na simulação (permanece idêntico)
        if self.simulation:
            quantity = self.calculate_quantity()
            if quantity is None:
                return None
            print(f"[SIMULAÇÃO] VENDA: {quantity}")
            return {"status": "simulated_sell", "quantity": quantity}

        # 2. OPERAÇÃO REAL: Consulta o saldo real disponível na Binance
        try:
            # Extrai o ativo base (Ex: de "BTCUSDT" extrai apenas "BTC")
            base_asset = self.symbol.replace("USDT", "")

            # Busca o saldo direto da API da Binance
            account_info = self.client.get_asset_balance(asset=base_asset)
            real_balance = float(account_info['free'])

            # Aplica o mesmo ajuste matemático para respeitar o step_size da exchange
            quantity = self._adjust_quantity(real_balance)

            print(f"[DEBUG VENDA] Saldo Real: {real_balance} | Ajustado para Venda: {quantity}")

            # Validação de segurança para quantidade mínima
            if quantity < self.min_qty:
                print(f"[ERRO VENDA] Saldo real em conta ({quantity}) é menor que o mínimo exigido ({self.min_qty})")
                return None

        except Exception as e:
            print(f"[ERRO] Falha ao consultar saldo real na Binance para venda: {e}")
            raise e # Lança o erro para o bloco except do main.py gerenciar

        # 3. Executa a venda no mercado real com precisão cirúrgica
        print(f"Executando VENDA REAL de {quantity} {base_asset}")

        order = self.client.order_market_sell(
            symbol=self.symbol,
            quantity=quantity
        )

        return order

    def _get_lot_size_filters(self):
        info = self.client.get_symbol_info(self.symbol)

        lot_size = next(f for f in info['filters'] if f['filterType'] == 'LOT_SIZE')

        step_size = float(lot_size['stepSize'])
        min_qty = float(lot_size['minQty'])

        return step_size, min_qty


    def _adjust_quantity(self, quantity):
        adjusted = math.floor(quantity / self.step_size) * self.step_size
        return round(adjusted, 6)
        #return math.floor(quantity / self.step_size) * self.step_size
