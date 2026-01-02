def get_index_bias(df):
    if len(df) < 50:
        return "CHOP"

    last = df.iloc[-1]
    prev = df.iloc[-2]

    if (
        last["close"] > last["vwap"] and
        last["ema_20"] > last["ema_50"] and
        last["ema_50"] > prev["ema_50"] and
        last["rsi"] > prev["rsi"]
    ):
        return "BULLISH"

    if (
        last["close"] < last["vwap"] and
        last["ema_20"] < last["ema_50"] and
        last["ema_50"] < prev["ema_50"] and
        last["rsi"] < prev["rsi"]
    ):
        return "BEARISH"

    return "CHOP"
