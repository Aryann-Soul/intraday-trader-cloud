import streamlit as st
from engine.data_loader import load_intraday_csv
from engine.indicators import add_indicators
from engine.index_bias import get_index_bias
from engine.signal_engine import generate_signal

st.set_page_config(layout="wide")

st.title("📊 Intraday Trading Dashboard (Personal)")
st.caption("5-min signals | Index aligned | Cloud hosted")

symbol = st.selectbox(
    "Select Instrument",
    ["NIFTY", "BANKNIFTY", "RELIANCE", "TCS"]
)

if st.button("Refresh Signal"):
    with st.spinner("Fetching NSE data..."):
        try:
            df = load_intraday_csv(symbol)
            df = add_indicators(df)

            bias = get_index_bias(df)
            signal, reason = generate_signal(df, bias)

            col1, col2, col3 = st.columns(3)
            col1.metric("Index Bias", bias)
            col2.metric("Signal", signal)
            col3.metric("Last Candle", str(df.iloc[-1]["datetime"]))

            st.success(reason)
            st.caption("Live NSE data")

        except Exception:
            try:
                # Use cached data if available
                df = load_intraday_csv(symbol)
                df = add_indicators(df)

                bias = get_index_bias(df)
                signal, reason = generate_signal(df, bias)

                col1, col2, col3 = st.columns(3)
                col1.metric("Index Bias", bias)
                col2.metric("Signal", signal)
                col3.metric("Last Candle", str(df.iloc[-1]["datetime"]))

                st.warning("Using last cached data (NSE temporarily blocked)")

            except Exception:
                st.error("No data available yet. Please wait and retry.")
