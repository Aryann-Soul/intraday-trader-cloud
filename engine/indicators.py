import pandas as pd
import pandas_ta as ta

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ema_20"] = ta.ema(df["close"], length=20)
    df["ema_50"] = ta.ema(df["close"], length=50)
    df["rsi"] = ta.rsi(df["close"], length=14)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)

    df["vwap"] = ta.vwap(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"]
    )

    df["vol_avg"] = df["volume"].rolling(20).mean()
    df["rel_volume"] = df["volume"] / df["vol_avg"]

    return df
