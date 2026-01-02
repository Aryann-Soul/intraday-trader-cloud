import streamlit as st
from engine.data_loader import load_intraday_csv
from engine.indicators import add_indicators
from engine.index_bias import get_index_bias
from engine.signal_engine import generate_signal
from datetime import datetime, time as dtime
import pytz
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("📊 Intraday Trading Dashboard (Personal)")
st.caption("5-min signals | Index aligned | Cloud hosted")

# Auto-refresh every 5 minutes (300 seconds)
st_autorefresh(interval=300000, key="auto_refresh")

def is_market_open():
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()
    return dtime(9, 15) <= now <= dtime(15, 30)


symbol = st.selectbox(
    "Select Instrument",
    ["NIFTY", "BANKNIFTY", "RELIANCE", "TCS"]
)

run = st.button("Refresh Signal") or True
if run:
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
            if not is_market_open():
                st.info("Market is currently closed. Intraday data will be available after 9:15 AM IST.")
            else:
                st.warning("Waiting for first valid NSE data. Please retry in 10–15 seconds.")
