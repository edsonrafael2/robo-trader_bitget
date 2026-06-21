# robo_trader
Objetivo deste robo_trader Proteger o capital investido, eliminar prejuizo, travar o lucro e deixar o lucro correr.
comando executado para rodar o test e o pthon identificar onde estavam as pastas importadas
#python -m tests.test_connection
#python -m tests.test_market
#python -m tests.test_strategy

Resumo de funcionalidade do Robo:

É robô um trader automatizado Spot, que:

analisa o mercado
decide quando entrar
executa compra
gerencia risco automaticamente
executa venda

Fluxo completo:

INÍCIO
  │
  ▼
Conectar Binance (.env)
  │
  ▼
Loop infinito (a cada X segundos)
  │
  ▼
Buscar candles (MarketData)
  │
  ▼
Tem posição aberta?
 ├── NÃO
 │     │
 │     ▼
 │   EntryStrategy
 │     │
 │     ▼
 │   Sinal de compra?
 │     │
 │   ├── NÃO → volta ao loop
 │   │
 │   └── SIM
 │         │
 │         ▼
 │     Executa COMPRA
 │         │
 │         ▼
 │     Cria RiskManagement
 │         │
 │         ▼
 │     in_position = True
 │
 └── SIM
       │
       ▼
   Atualiza preço atual
       │
       ▼
   RiskManagement.update()
       │
       ▼
   Resultado?
       │
   ├── HOLD → continua
   │
   ├── TAKE_PROFIT
   │       ▼
   │     VENDA
   │
   └── STOP
           ▼
         VENDA
           
       ▼
   in_position = False

  ▼
Volta ao loop


Modulos:

| Módulo               | Função              |
| -------------------- | ------------------- |
| `binance_client.py`  | conexão com API     |
| `market_data.py`     | dados do mercado    |
| `entry_strategy.py`  | decide entrada      |
| `risk_management.py` | controla stop/lucro |
| `order_executor.py`  | executa ordens      |
| `main.py`            | orquestra tudo      |



Estratégia atual:

Entrada:
tendência + rompimento (via candles)
Saída:
STOP LOSS
BREAK EVEN
PROFIT LOCK
TAKE PROFIT OU
TRAILING STOP

O robô permite:

✔ mudar par
✔ mudar valor investido
✔ mudar estratégia
✔ mudar tipo de saída (TP ou TRAILING)

Bloco - SIMULAÇÃO
Para Efetivar a simulação o arquivo SIMULATION_MODE predisa esta True em config/sitting e
no main depois do if, comentar signal = entry_strategy.check_entry(), e descomentar #signal = True  # FORÇAR TESTE e
return "TAKE_PROFIT" -> Colocado na linha 32 do risk_managenment para tornar a venda na simulação mais rapida


