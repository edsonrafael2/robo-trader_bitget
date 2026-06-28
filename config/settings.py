# PAR
SYMBOL = "BTCUSDT"

# TIMEFRAME
TIMEFRAME = "5m"

#
SANDBOX = False

# RISCO
STOP_LOSS = 0.01
BREAK_EVEN = 0.006 # antes -> 0.005
PROFIT_LOCK = 0.005 #Estava 0.002 depois 0.004

# LUCRO
TAKE_PROFIT = 0.012 #Anes -> 0.01
TRAILING_STOP = 0.005#Antes -> 0.004

# VALOR POR OPERAÇÃO
TRADE_MODE = "PERCENT" # FIXED
TRADE_PERCENT = 0.50
TRADE_AMOUNT = 50 # valor em USDT por operação

#SIMULATION_MODE = True # Adicionar no futuro

# MODO DE SAÍDA
# "TP" = fechar no take profit
# "TRAILING" = iniciar trailing stop
EXIT_MODE = "TRAILING"

SIMULATION_MODE = False #Usado no simulador

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
