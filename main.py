
#New main
import time
from datetime import datetime

from config.settings import SYMBOL, TIMEFRAME, TRADE_AMOUNT

from exchange.binance_client import BinanceClient
from market.market_data import MarketData
from strategies.entry_strategy import EntryStrategy
from strategies.risk_management import RiskManagement
from trading.order_executor import OrderExecutor
from utils.logger import log
from utils.telegram import send_telegram


def main():

    # cria cliente da Binance
    binance = BinanceClient()
    client = binance.client

    # módulos do robô
    market_data = MarketData()
    order_executor = OrderExecutor(client, SYMBOL, TRADE_AMOUNT)

    in_position = False
    risk_manager = None
    entry_price = None
    quantity = None

    log("Robô iniciado...")


    while True:

        print(f"[{datetime.now()}] Robo ativo - Analisando mercado....", end="\r")

        try:
            # busca candles com proteção
            candles = market_data.get_klines(SYMBOL, TIMEFRAME, 100)
        except Exception as e:
            log(f"Erro ao buscar candles: {e}")
            print("Erro de conexão com Binance. Tentando novamente em 30 segundos...")
            time.sleep(30)# almentar o tempo para 30 s
            continue

        try:
            if not in_position:

                entry_strategy = EntryStrategy(candles)

                signal = entry_strategy.check_entry()
                #signal = True  # FORÇAR TESTE

                # ===== TESTE MANUAL =====
                # signal = True
                # =========================

                if signal:

                    log("Sinal de COMPRA detectado")
                    print("Sinal de COMPRA detectado")

                    quantity = order_executor.calculate_quantity()
                    order_executor.buy()

                    entry_price = order_executor.get_price()

                    log(f"Compra executada em {entry_price}")

                    try:
                        send_telegram(
                            f"📈 COMPRA {SYMBOL}\n"
                            f"💰 Entrada: {entry_price}\n"
                            f"🪙 Quantidade: {quantity:.6f}"
                        )
                    except Exception as e:
                        log(f"Erro ao enviar Telegram (compra): {e}")

                    risk_manager = RiskManagement(entry_price)

                    in_position = True

            else:
                try:
                    current_price = order_executor.get_price()
                except Exception as e:
                    log(f"Erro ao buscar preço atual: {e}")
                    print("Erro ao buscar preço. Tentando novamente em 15 segundos...")
                    time.sleep(15)
                    continue

                state = risk_manager.update(current_price)

                log(f"Preço: {current_price} | Estado: {state}")

                if state in ["TAKE_PROFIT", "STOP"]:

                    profit_pct = ((current_price - entry_price) / entry_price) * 100
                    profit_value = (current_price - entry_price) * quantity

                    log("Saindo da posição")

                    order_executor.sell()

                    log(
                        f"Venda executada | "
                        f"Resultado: {profit_pct:.2f}% | "
                        f"Valor: {profit_value:.2f} USDT"
                    )

                    try:
                        send_telegram(
                            f"📊 VENDA {SYMBOL}\n"
                            f"{'🟢 LUCRO' if profit_pct > 0 else '🔴 PREJUÍZO'}\n"
                            f"💰 Resultado: {profit_pct:.2f}%\n"
                            f"💵 Valor: {profit_value:.2f} USDT\n"
                            f"💵 Entrada: {entry_price}\n"
                            f"💵 Saída: {current_price}"
                        )
                    except Exception as e:
                        log(f"Erro ao enviar Telegram (venda): {e}")

                    in_position = False
                    risk_manager = None
                    entry_price = None
                    quantity = None

        except Exception as e:
            log(f"Erro inesperado no loop principal: {e}")
            print("Erro inesperado. O robô vai continuar rodando...")
            time.sleep(15)
            continue

        time.sleep(15) # Ateração feita de 10 paraa 15s para evitar Rate Limit ao buscar as candles.


if __name__ == "__main__":
    main()
#Old main

# import time
# from utils.logger import log
# from utils.telegram import send_telegram

# from config.settings import SYMBOL, TIMEFRAME, TRADE_AMOUNT

# from exchange.binance_client import BinanceClient
# from market.market_data import MarketData
# from strategies.entry_strategy import EntryStrategy
# from strategies.risk_management import RiskManagement
# from trading.order_executor import OrderExecutor


# def main():

#     # cria cliente da Binance
#     binance = BinanceClient()
#     client = binance.client

#     # módulos do robô
#     market_data = MarketData()
#     order_executor = OrderExecutor(client, SYMBOL, TRADE_AMOUNT)

#     in_position = False
#     risk_manager = None
#     print("Robô iniciado...")

#     while True:

#         #candles = market_data.get_candles()
#         candles = market_data.get_klines(SYMBOL, TIMEFRAME, 100)

#         if not in_position:

#             entry_strategy = EntryStrategy(candles)

#             signal = entry_strategy.check_entry()
#             #signal = True  # FORÇAR TESTE

#             if signal:
#                 log("Sinal de COMPRA detectado")#Usado no log
#                 print("Sinal de COMPRA detectado")
                

#                 order_executor.buy()

#                 quantity = order_executor.calculate_quantity()
#                 entry_price = order_executor.get_price()
#                 log(f"Compra executada em {entry_price}")# Usado no log

#                 risk_manager = RiskManagement(entry_price)

            
#                 in_position = True

#         else:

#             current_price = order_executor.get_price()

#             state = risk_manager.update(current_price)

#             if state in ["TAKE_PROFIT", "STOP"]:
#                 profit_pct = ((current_price - entry_price) / entry_price) * 100
#                 profit_value = (current_price - entry_price) * quantity
#                 log("Saindo da posição")# Usado no log
#                 print("Saindo da posição")

#                 order_executor.sell()#Usado no log
#                 #log("Venda executada")
#                 log(f"Venda executada | Resultado: {profit_pct:.2f}%")

#                 send_telegram(
#                     f"📊 VENDA {SYMBOL}\n"
#                     f"{'🟢 LUCRO' if profit_pct > 0 else '🔴 PREJUÍZO'}\n"
#                     f"💰 Resultado: {profit_pct:.2f}%\n"
#                     f"💵 Valor: {profit_value:.2f} USDT\n"
#                     f"💵 Entrada: {entry_price}\n"
#                     f"💵 Saída: {current_price}"       
                    
#                 )


#                 in_position = False

#         time.sleep(10)


# if __name__ == "__main__":
#     main()
