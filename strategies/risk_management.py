from config.settings import (
    STOP_LOSS,
    BREAK_EVEN,
    PROFIT_LOCK,
    TAKE_PROFIT,
    TRAILING_STOP,
    EXIT_MODE
)


class RiskManagement:

    def __init__(self, entry_price):

        self.entry_price = entry_price

        # níveis iniciais
        self.stop_loss_price = entry_price * (1 - STOP_LOSS)
        self.break_even_trigger = entry_price * (1 + BREAK_EVEN)
        self.profit_lock_trigger = entry_price * (1 + BREAK_EVEN)

        self.take_profit_price = entry_price * (1 + TAKE_PROFIT)

        self.trailing_distance = TRAILING_STOP

        self.highest_price = entry_price
        self.current_stop = self.stop_loss_price

        self.exit_mode = EXIT_MODE

    def update(self, current_price):
        #return "TAKE_PROFIT" # Serve para adiantar o processo de simulação
        # atualizar maior preço
        if current_price > self.highest_price:
            self.highest_price = current_price

        # BREAK EVEN
        if current_price >= self.break_even_trigger:
            self.current_stop = max(self.current_stop, self.entry_price)

        # PROFIT LOCK
        if current_price >= self.profit_lock_trigger:
            locked_price = self.entry_price * (1 + PROFIT_LOCK)
            self.current_stop = max(self.current_stop, locked_price)

        # TAKE PROFIT
        if current_price >= self.take_profit_price:

            if self.exit_mode == "TP":
                return "TAKE_PROFIT"

            if self.exit_mode == "TRAILING":

                trailing_stop = self.highest_price * (1 - self.trailing_distance)
                self.current_stop = max(self.current_stop, trailing_stop)

        # STOP LOSS / TRAILING STOP
           
        if current_price <= self.current_stop:
            return "STOP"

        return "HOLD"