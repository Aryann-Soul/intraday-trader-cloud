import streamlit as st
from streamlit_autorefresh import st_autorefresh
from engine.scanner import scan_symbols
from datetime import datetime, time as dtime
import pytz

st.set_page_config(layout="wide")

st.title("📊 Intraday Trading Dashboard")
st.caption("Auto-refresh | Index aligned | Cloud hosted")

# Auto refresh every 5 minutes
st_autorefresh(interval=300000, key="auto_refresh")


def is_market_open():
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()
    return dtime(9, 15) <= now <= dtime(15, 30)


MODE = st.radio("Mode", ["Scanner"], horizontal=True)

if not is_market_open():
    st.info("Market closed. Data updates after 9:15 AM IST.")
    st.stop()

NSE_200 = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
    "SBIN", "ITC", "LT", "AXISBANK", "KOTAKBANK"
]

with st.spinner("Scanning market..."):
    results = scan_symbols(NSE_200)

if results:
    st.dataframe(results, use_container_width=True)
else:
    st.warning("No high-quality setups right now.")
