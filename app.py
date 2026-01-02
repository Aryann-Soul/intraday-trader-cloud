import streamlit as st
from streamlit_autorefresh import st_autorefresh
from engine.scanner import scan_symbols
from datetime import datetime, time as dtime
import pytz

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Intraday Trading Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Auto refresh every 5 minutes
# --------------------------------------------------
st_autorefresh(interval=300000, key="auto_refresh")

# --------------------------------------------------
# Custom CSS (NO triple-quoted issues)
# --------------------------------------------------
st.markdown(
    "<style>"
    ".block-container{padding-top:1.2rem;}"
    "h1{font-size:1.8rem;font-weight:700;}"
    ".card{background-color:#161B22;border-radius:14px;padding:16px;"
    "margin-bottom:16px;box-shadow:0 0 0 1px #30363d;}"
    ".badge-high{color:#ff6b6b;font-weight:700;}"
    ".badge-normal{color:#00C805;font-weight:700;}"
    "</style>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("📊 Intraday Trading Dashboard")
st.caption("Auto-refresh | Index aligned | Cloud hosted")

# --------------------------------------------------
# Market hours check (IST, Streamlit Cloud safe)
# --------------------------------------------------
def is_market_open():
    utc_now = datetime.utcnow()
    india = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(india)
    now = ist_now.time()
    return dtime(9, 20) <= now <= dtime(15, 30)

# --------------------------------------------------
# Signal types card
# --------------------------------------------------
st.markdown(
    "<div class='card'>"
    "<h3>Signal Types</h3>"
    "<p>🔥 <span class='badge-high'>HIGH MOMENTUM</span> — Strong volume & volatility (fast moves)</p>"
    "<p>✅ <span class='badge-normal'>NORMAL</span> — Clean trend-aligned setups</p>"
    "</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Market closed guard
# --------------------------------------------------
if not is_market_open():
    st.info("Market not active. Scanner runs between 9:20 AM – 3:30 PM IST.")
    st.stop()

# --------------------------------------------------
# Symbols universe
# --------------------------------------------------
NSE_200 = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
    "SBIN", "ITC", "LT", "AXISBANK", "KOTAKBANK"
]

# --------------------------------------------------
# Scanner execution
# --------------------------------------------------
with st.spinner("Scanning market..."):
    results = scan_symbols(NSE_200)

# --------------------------------------------------
# Scanner section
# --------------------------------------------------
st.markdown("<h3>📈 Live Market Scanner</h3>", unsafe_allow_html=True)

if results:
    high_count = sum(1 for r in results if r["Type"] == "HIGH MOMENTUM")
    normal_count = sum(1 for r in results if r["Type"] == "NORMAL")

    st.markdown(
        "<div class='card'>"
        "<b>Market Summary</b><br>"
        f"🔥 High Momentum: {high_count}<br>"
        f"✅ Normal Setups: {normal_count}"
        "</div>",
        unsafe_allow_html=True
    )

    st.dataframe(
        results,
        use_container_width=True,
        height=420
    )
else:
    st.warning("No high-quality setups right now.")
