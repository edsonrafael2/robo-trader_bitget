# robo-trader_bitget
O que mudamos :
data/maket_data.py depois
exchange/bitget_client.py depois
trading/order_executor.py e
main.py

Bloco - SIMULAÇÃO Para Efetivar a simulação:
1 - SIMULATION_MODE precisa esta True em config/sitting
2 - No main depois do if, comentar signal = entry_strategy.check_entry(), e descomentar #signal = True # FORÇAR TESTE 
3 - E return "TAKE_PROFIT" -> Colocado na linha 32 do risk_managenment para tornar a venda na simulação mais rapida.