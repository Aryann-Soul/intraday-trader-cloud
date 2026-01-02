import streamlit as st
from streamlit_autorefresh import st_autorefresh
from engine.scanner import scan_symbols
from datetime import datetime, time as dtime
import pytz

st.set_page_config(layout="wide")

st.title("📊 Intraday Trading Dashboard")
st.caption("Auto-refresh | Index aligned | Cloud hosted")

st_autorefresh(interval=300000, key="auto")


def is_market_open():
    utc_now = datetime.utcnow()
    india = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(india)
    now = ist_now.time()
    return dtime(9, 20) <= now <= dtime(15, 30)


st.markdown("""
### Signal Types
- 🔥 **HIGH MOMENTUM** → Strong volume + volatility (fast moves)
- ✅ **NORMAL** → Clean trend-aligned setups
""")

if not is_market_open():
    st.info("Market not active. Scanner runs between 9:20 AM – 3:30 PM IST.")
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
