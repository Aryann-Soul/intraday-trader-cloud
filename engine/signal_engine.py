BANK_STOCKS = [
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "AXISBANK",
    "KOTAKBANK"
]


def generate_signal(df, index_bias, symbol):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Bank stock alignment
    if symbol in BANK_STOCKS and index_bias != "BANKNIFTY":
        return "NO TRADE", "Bank stock not aligned with BANKNIFTY"

    if index_bias == "CHOP":
        return "NO TRADE", "Index not trending"

    volume_ok = last["rel_volume"] >= 1.5
    atr_ok = last["atr"] <= df["atr"].rolling(20).mean().iloc[-1] * 1.8

    if (
        index_bias == "BULLISH"
        and last["close"] > last["vwap"]
        and last["ema_20"] > last["ema_50"]
        and last["ema_50"] > prev["ema_50"]
        and volume_ok
        and atr_ok
    ):
        return "LONG", "Trend + VWAP + Volume"

    if (
        index_bias == "BEARISH"
        and last["close"] < last["vwap"]
        and last["ema_20"] < last["ema_50"]
        and last["ema_50"] < prev["ema_50"]
        and volume_ok
        and atr_ok
    ):
        return "SHORT", "Trend + VWAP + Volume"

    return "NO TRADE", "Conditions not met"
