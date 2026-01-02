from engine.data_loader import load_intraday_csv
from engine.indicators import add_indicators
from engine.index_bias import get_index_bias
from engine.signal_engine import generate_signal
from engine.confidence import score_signal


def scan_symbols(symbols):
    results = []

    for symbol in symbols:
        try:
            df = load_intraday_csv(symbol)
            df = add_indicators(df)

            bias = get_index_bias(df)
            signal, reason = generate_signal(df, bias, symbol)
            confidence, risk = score_signal(df, signal)

            if signal != "NO TRADE":
                results.append({
                    "Symbol": symbol,
                    "Signal": signal,
                    "Confidence": confidence,
                    "Risk": risk,
                    "Reason": reason
                })

        except Exception:
            continue

    return results
