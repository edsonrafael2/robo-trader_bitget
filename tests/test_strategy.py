from strategies.strategy_engine import StrategyEngine

entry_price = 100

strategy = StrategyEngine(entry_price)

prices = [100.2, 100.8, 101.2, 101.6, 102, 103, 102.5, 102]

for price in prices:

    stop = strategy.update(price)

    print(f"Preço: {price} | Stop atual: {round(stop,4)}")