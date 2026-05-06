
import time

from config.settings import SYMBOLS, TIMEFRAME, TRADE_AMOUNT, COOLDOWN_AFTER_SELL

from exchange.bitget_client import BitgetClient
from market.market_data import MarketData
from strategies.entry_strategy import EntryStrategy
from strategies.risk_management import RiskManagement
from trading.order_executor import OrderExecutor
from utils.logger import log
from utils.telegram import send_telegram



def main():

    # cliente Bitget
    bitget = BitgetClient()
    client = bitget

    market_data = MarketData()

    in_position = False
    risk_manager = None
    entry_price = None
    quantity = None
    last_sell_time = 0
    current_symbol = None
    cooldown_active = False

    log("🤖 Robô Bitget iniciado e monitorando mercado", telegram=True)

    while True:

        try:

            # =========================
            # 🔎 BUSCA ENTRADA (MULTIPAR)
            # =========================
            if not in_position:

                # 🔥 CONTROLE DE COOLDOWN
                if time.time() - last_sell_time < COOLDOWN_AFTER_SELL:

                    remaining = int(COOLDOWN_AFTER_SELL - (time.time() - last_sell_time))

                    if not cooldown_active:
                        log(f"⏳ Em cooldown - faltam {remaining} segundos", telegram=True)
                        cooldown_active = True
                    else:
                        print(f"⏳ Cooldown... {remaining}s restantes")

                    time.sleep(10)
                    continue

                # saiu do cooldown
                if cooldown_active:
                    log("🤖 Robô monitorando mercado novamente", telegram=True)
                    cooldown_active = False

                for symbol in SYMBOLS:

                    try:
                        candles = market_data.get_klines(symbol, TIMEFRAME, 100)
                    except Exception as e:
                        log(f"Erro ao buscar candles de {symbol}: {e}")
                        continue

                    entry_strategy = EntryStrategy(candles)
                    signal = entry_strategy.check_entry()

                    if signal:

                        log(f"📈 Sinal de COMPRA detectado em {symbol}", telegram=True)

                        current_symbol = symbol
                        order_executor = OrderExecutor(client, symbol, TRADE_AMOUNT)

                        quantity = order_executor.calculate_quantity()
                        order_executor.buy()

                        entry_price = order_executor.get_price()

                        log(f"Compra executada em {entry_price} ({symbol})")

                        try:
                            send_telegram(
                                f"📈 COMPRA {symbol}\n"
                                f"💰 Entrada: {entry_price}\n"
                                f"🪙 Quantidade: {quantity:.6f}"
                            )
                        except Exception as e:
                            log(f"Erro ao enviar Telegram (compra): {e}")

                        risk_manager = RiskManagement(entry_price)

                        in_position = True

                        break

            # =========================
            # 📊 GERENCIA POSIÇÃO
            # =========================
            else:

                try:
                    order_executor = OrderExecutor(client, current_symbol, TRADE_AMOUNT)
                    current_price = order_executor.get_price()
                except Exception as e:
                    log(f"Erro ao buscar preço atual: {e}")
                    time.sleep(15)
                    continue

                state = risk_manager.update(current_price)

                log(f"{current_symbol} | Preço: {current_price} | Estado: {state}")

                if state in ["TAKE_PROFIT", "STOP"]:

                    profit_pct = ((current_price - entry_price) / entry_price) * 100
                    profit_value = (current_price - entry_price) * quantity

                    log("Saindo da posição")

                    order_executor.sell()

                    last_sell_time = time.time()

                    log(
                        f"📊 Venda executada | Resultado: {profit_pct:.2f}% | Valor: {profit_value:.2f} USDT"
                    )

                    try:
                        send_telegram(
                            f"📊 VENDA {current_symbol}\n"
                            f"{'🟢 LUCRO' if profit_pct > 0 else '🔴 PREJUÍZO'}\n"
                            f"💰 Resultado: {profit_pct:.2f}%\n"
                            f"💵 Valor: {profit_value:.2f} USDT\n"
                            f"💵 Entrada: {entry_price}\n"
                            f"💵 Saída: {current_price}"
                        )
                    except Exception as e:
                        log(f"Erro ao enviar Telegram (venda): {e}")

                    # reset
                    in_position = False
                    risk_manager = None
                    entry_price = None
                    quantity = None
                    current_symbol = None

        except Exception as e:
            log(f"Erro inesperado no loop principal: {e}")
            print("Erro inesperado. O robô vai continuar rodando...")
            time.sleep(15)
            continue

        time.sleep(10)


if __name__ == "__main__":
    main()





# import time

# from config.settings import SYMBOLS, TIMEFRAME, TRADE_AMOUNT, COOLDOWN_AFTER_SELL

# from exchange.binance_client import BinanceClient
# from market.market_data import MarketData
# from strategies.entry_strategy import EntryStrategy
# from strategies.risk_management import RiskManagement
# from trading.order_executor import OrderExecutor
# from utils.logger import log
# from utils.telegram import send_telegram
# #cooldown_active = False


# def main():

#     # cliente Binance
#     binance = BinanceClient()
#     client = binance.client

#     market_data = MarketData()

#     in_position = False
#     risk_manager = None
#     entry_price = None
#     quantity = None
#     last_sell_time = 0
#     current_symbol = None

#     log("🤖 Robô iniciado e monitorando mercado", telegram=True)

#     while True:

#         try:

#             # =========================
#             # 🔎 BUSCA ENTRADA (MULTIPAR)
#             # =========================
#             if not in_position:

#                 for symbol in SYMBOLS:
#                     print(f"Buscando sinal em {symbol}...         ", end='\r')

#                     try:
#                         candles = market_data.get_klines(symbol, TIMEFRAME, 100)
#                     except Exception as e:
#                         log(f"Erro ao buscar candles de {symbol}: {e}")
#                         continue

#                     entry_strategy = EntryStrategy(candles)
#                     signal = entry_strategy.check_entry()

#                     if signal:

#                         if time.time() - last_sell_time < COOLDOWN_AFTER_SELL:
#                             print(f"Cooldown ativo... aguardando {COOLDOWN_AFTER_SELL//60} min")
#                             time.sleep(10)
#                             break

#                         log(f"📈 Sinal de COMPRA detectado em {symbol}", telegram=True)

#                         current_symbol = symbol
#                         order_executor = OrderExecutor(client, symbol, TRADE_AMOUNT)

#                         quantity = order_executor.calculate_quantity()
#                         order_executor.buy()

#                         entry_price = order_executor.get_price()

#                         log(f"Compra executada em {entry_price} ({symbol})")

#                         try:
#                             send_telegram(
#                                 f"📈 COMPRA {symbol}\n"
#                                 f"💰 Entrada: {entry_price}\n"
#                                 f"🪙 Quantidade: {quantity:.6f}"
#                             )
#                         except Exception as e:
#                             log(f"Erro ao enviar Telegram (compra): {e}")

#                         risk_manager = RiskManagement(entry_price)

#                         in_position = True

#                         break  # 🔥 para de procurar outros pares

#             # =========================
#             # 📊 GERENCIA POSIÇÃO
#             # =========================
#             else:

#                 try:
#                     current_price = OrderExecutor(client, current_symbol, TRADE_AMOUNT).get_price()
#                 except Exception as e:
#                     log(f"Erro ao buscar preço atual: {e}")
#                     time.sleep(15)
#                     continue

#                 state = risk_manager.update(current_price)

#                 log(f"{current_symbol} | Preço: {current_price} | Estado: {state}")

#                 if state in ["TAKE_PROFIT", "STOP"]:

#                     profit_pct = ((current_price - entry_price) / entry_price) * 100
#                     profit_value = (current_price - entry_price) * quantity

#                     log("Saindo da posição")

#                     OrderExecutor(client, current_symbol, TRADE_AMOUNT).sell()

#                     last_sell_time = time.time()

#                     log(
#                         f"📊 Venda executada | Resultado: {profit_pct:.2f}% | Valor: {profit_value:.2f} USDT"
#                     )

#                     try:
#                         send_telegram(
#                             f"📊 VENDA {current_symbol}\n"
#                             f"{'🟢 LUCRO' if profit_pct > 0 else '🔴 PREJUÍZO'}\n"
#                             f"💰 Resultado: {profit_pct:.2f}%\n"
#                             f"💵 Valor: {profit_value:.2f} USDT\n"
#                             f"💵 Entrada: {entry_price}\n"
#                             f"💵 Saída: {current_price}"
#                         )
#                     except Exception as e:
#                         log(f"Erro ao enviar Telegram (venda): {e}")

#                     # reset
#                     in_position = False
#                     risk_manager = None
#                     entry_price = None
#                     quantity = None
#                     current_symbol = None

#         except Exception as e:
#             log(f"Erro inesperado no loop principal: {e}")
#             print("Erro inesperado. O robô vai continuar rodando...")
#             time.sleep(15)
#             continue

#         time.sleep(10)


# if __name__ == "__main__":
#     main()

