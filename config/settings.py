# PAR
#SYMBOL = "BTCUSDT" # Substituido por multiplos pares
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT"]

# TIMEFRAME
TIMEFRAME = "5m"

# RISCO
STOP_LOSS = 0.01
BREAK_EVEN = 0.005
PROFIT_LOCK = 0.004 #Estava 0.002

# LUCRO
TAKE_PROFIT = 0.01
TRAILING_STOP = 0.004

# TEMPO ENTRE OPERAÇÕES
COOLDOWN_AFTER_SELL = 300

# VALOR POR OPERAÇÃO
TRADE_MODE = "PERCENT" #FIXED -> Quando quiser operar com valor fixo.
TRADE_PERCENT = 0.85   # 20%
TRADE_AMOUNT = 50 # valor em USDT por operação

#SIMULATION_MODE = True # Adicionar no futuro

# MODO DE SAÍDA
# "TP" = fechar no take profit
# "TRAILING" = iniciar trailing stop
EXIT_MODE = "TRAILING"

SIMULATION_MODE = True #Usado no simulador

# SIMULATION_MODE = True → NÃO envia ordens simulando
# SIMULATION_MODE = False → envia ordens não simulando


# # PAR DE NEGOCIAÇÃO
# SYMBOL = "BTCUSDT"

# # TIMEFRAME
# TIMEFRAME = "5m"

# # RISCO
# STOP_LOSS = 0.01
# BREAK_EVEN = 0.007 #0.005
# PROFIT_LOCK = 0.003 #0.002

# # LUCRO
# TAKE_PROFIT = 0.015 #0.01
# TRAILING_STOP = 0.005 #0.004


###################



# # TIMEFRAME DO MERCADO
# TIMEFRAME = "5m"

# # GERENCIAMENTO DE RISCO
# STOP_LOSS = 0.01        # 1%
# BREAK_EVEN = 0.007      # 0.7% Mudar depois para 0.005 permitir mais espaço , ou

# # OBJETIVO DE LUCRO
# TAKE_PROFIT = 0.015     # 1.5% Mudar para 1% vai garantir capturas menores

# # TRAILING STOP
# TRAILING_STOP = 0.005   # 0.5%