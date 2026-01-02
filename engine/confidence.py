def score_signal(df, signal):
    """
    Returns confidence (0–100) and risk label
    """
    latest = df.iloc[-1]

    score = 0

    if signal in ["LONG", "SHORT"]:
        score += 40

    if abs(latest["ema_20"] - latest["ema_50"]) / latest["close"] > 0.002:
        score += 20

    if latest["rel_volume"] >= 2:
        score += 20
    elif latest["rel_volume"] >= 1.5:
        score += 10

    if latest["atr"] < df["atr"].rolling(20).mean().iloc[-1]:
        score += 20

    if score >= 75:
        risk = "LOW"
    elif score >= 55:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return min(score, 100), risk
