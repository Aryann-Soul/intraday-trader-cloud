import streamlit as st
from streamlit_autorefresh import st_autorefresh
from engine.scanner import scan_symbols
from datetime import datetime, time as dtime
import pytz

# --------------------------------------------------
# Page config
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
# Custom CSS for professional trading UI
# --------------------------------------------------
st.markdown("""
<style>

/* Remove top padding */
.block-container {
    padding-top: 1.2rem;
}

/* Main title */
h1 {
    font-size: 1.8rem;
    font-weight: 700;
}

/* Card container */
.card {
    background-color: #161B22;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 0 0 1px #30363d;
}

/* Badges */
.badge-high {
    color: #ff6b6b;
    font-weight: 700;
}
.badge-normal {
    color: #00C805;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

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
# Signal legend card
# --------------------------------------------------
st.markdown("""
<div class="card">
<h3>Signal Types
