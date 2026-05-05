
from market.market_data import MarketData
from strategies.entry_strategy import EntryStrategy
from strategies.risk_management import RiskManagement
from config.settings import SYMBOL, TIMEFRAME


class StrategyEngine:

    def __init__(self):

        self.market = MarketData()
        self.position_open = False
        self.risk_manager = None

    def run_cycle(self):

        # pegar candles
        candles = self.market.get_klines(SYMBOL, TIMEFRAME, 100)

        # pegar preço atual
        current_price = self.market.get_price(SYMBOL)

        # se não tem posição aberta → verificar entrada
        if not self.position_open:

            entry_strategy = EntryStrategy(candles)

            signal = entry_strategy.check_entry()

            if signal:

                print("Sinal de COMPRA detectado")

                self.position_open = True
                self.risk_manager = RiskManagement(current_price)

                print(f"Entrada simulada em {current_price}")

        # se já existe posição → gerenciar risco
        else:

            result = self.risk_manager.update(current_price)

            print(f"Preço: {current_price} | Estado: {result}")

            if result in ["STOP", "TAKE_PROFIT"]:

                print("Saindo da posição")

                self.position_open = False
                self.risk_manager = None






# from config.settings import (
#     STOP_LOSS,
#     BREAK_EVEN,
#     TAKE_PROFIT,
#     TRAILING_STOP
# )


# class StrategyEngine:

#     def __init__(self, entry_price):

#         self.entry_price = entry_price

#         # níveis da estratégia
#         self.stop_loss_price = entry_price * (1 - STOP_LOSS)
#         self.break_even_trigger = entry_price * (1 + BREAK_EVEN)
#         self.take_profit_trigger = entry_price * (1 + TAKE_PROFIT)

#         # trailing
#         self.trailing_distance = TRAILING_STOP
#         self.highest_price = entry_price

#         # stop atual começa no stop loss
#         self.current_stop = self.stop_loss_price

#     def update(self, current_price):

#         # atualizar maior preço
#         if current_price > self.highest_price:
#             self.highest_price = current_price

#         # BREAK EVEN
#         if current_price >= self.break_even_trigger:
#             self.current_stop = max(self.current_stop, self.entry_price)

#         # TAKE PROFIT ATINGIDO
#         if current_price >= self.take_profit_trigger:

#             trailing_stop = self.highest_price * (1 - self.trailing_distance)

#             self.current_stop = max(self.current_stop, trailing_stop)

#         return self.current_stop