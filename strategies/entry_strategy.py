import pandas as pd

EMA_PERIOD = 50
ATR_PERIOD = 14
ATR_FILTER = 0.004


class EntryStrategy:

    def __init__(self, candles):

        self.df = self._prepare_dataframe(candles)

    def _prepare_dataframe(self, candles):

        df = pd.DataFrame(candles, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","qav","num_trades","taker_base_vol",
            "taker_quote_vol","ignore"
        ])

        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)

        return df

    def calculate_indicators(self):

        self.df["ema50"] = self.df["close"].ewm(span=EMA_PERIOD).mean()

        high_low = self.df["high"] - self.df["low"]
        high_close = abs(self.df["high"] - self.df["close"].shift())
        low_close = abs(self.df["low"] - self.df["close"].shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)

        true_range = ranges.max(axis=1)

        self.df["atr"] = true_range.rolling(ATR_PERIOD).mean()

    def check_entry(self):

        self.calculate_indicators()

        last = self.df.iloc[-1]
        prev = self.df.iloc[-2]

        # Tendência
        trend = last["close"] > last["ema50"]

        # Volatilidade
        atr_ok = last["atr"] > (last["close"] * ATR_FILTER)

        # Rompimento
        breakout = last["close"] > prev["high"]

        if trend and atr_ok and breakout:
            return True

        return False