def classify_signal(df, signal):
    if signal == "NO TRADE":
        return "NO TRADE", 0

    latest = df.iloc[-1]
    confidence = 40  # base

    if latest["rel_volume"] >= 2.5:
        confidence += 30
    elif latest["rel_volume"] >= 1.5:
        confidence += 15

    atr_ratio = latest["atr"] / df["atr"].rolling(20).mean().iloc[-1]
    if atr_ratio >= 1.5:
        confidence += 20
    elif atr_ratio >= 1.1:
        confidence += 10

    confidence = min(confidence, 100)

    if confidence >= 75:
        return "HIGH MOMENTUM", confidence
    elif confidence >= 50:
        return "NORMAL", confidence
    else:
        return "NO TRADE", confidence
