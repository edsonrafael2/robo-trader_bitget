from strategies.strategy_engine import StrategyEngine
import time

engine = StrategyEngine()

while True:

    print("Executando ciclo do robô...")
    
    engine.run_cycle()

    time.sleep(10)