import streamlit as st
from streamlit_autorefresh import st_autorefresh
from engine.scanner import scan_symbols
from datetime import datetime, time as dtime
import pytz
import pandas as pd

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Intraday Trading Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Auto refresh (5 min)
# --------------------------------------------------
st_autorefresh(interval=300000, key="auto_refresh")

# --------------------------------------------------
# Safe CSS (NO triple quotes)
# --------------------------------------------------
st.markdown(
    "<style>"
    ".block-container{padding-top:1rem;}"
    "h1{font-size:1.7rem;font-weight:700;}"
    ".card{background:#161B22;border-radius:14px;padding:14px;margin-bottom:14px;"
    "box-shadow:0 0 0 1px #30363d;}"
    ".status{background:#0d4f8b;padding:10px;border-radius:10px;margin-bottom:14px;}"
    ".high{color:#ff6b6b;font-weight:700;}"
    ".normal{color:#00C805;font-weight:700;}"
    "</style>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("📊 Intraday Trading Dashboard")
st.caption("Auto-refresh | Index aligned | Cloud hosted")

# --------------------------------------------------
# Time helpers
# --------------------------------------------------
def get_ist_time():
    utc_now = datetime.utcnow()
    india = pytz.timezone("Asia/Kolkata")
    return utc_now.replace(tzinfo=pytz.utc).astimezone(india)

def is_market_open():
    now = get_ist_time().time()
    return dtime(9, 20) <= now <= dtime(15, 30)

# --------------------------------------------------
# Top status bar
# --------------------------------------------------
ist_now = get_ist_time()
st.markdown(
    "<div class='status'>"
    f"🕒 IST Time: <b>{ist_now.strftime('%H:%M:%S')}</b> | "
    "🔄 Auto-refresh: 5 min"
    "</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Tabs (APP STYLE NAVIGATION)
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Scanner", "⭐ Watchlist", "📊 Summary"])

# ==================================================
# TAB 1 — SCANNER
# ==================================================
with tab1:

    st.markdown(
        "<div class='card'>"
        "<b>Signal Types</b><br>"
        "🔥 <span class='high'>HIGH MOMENTUM</span> — Fast moves<br>"
        "✅ <span class='normal'>NORMAL</span> — Clean setups"
        "</div>",
        unsafe_allow_html=True
    )

    if not is_market_open():
        st.info("Market not active. Scanner runs between 9:20 AM – 3:30 PM IST.")
        st.stop()

    # Controls
    compact = st.toggle("📱 Compact / Pro mode", value=False)

    NSE_200 = [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
        "SBIN", "ITC", "LT", "AXISBANK", "KOTAKBANK"
    ]

    with st.spinner("Scanning market..."):
        results = scan_symbols(NSE_200)

    st.markdown("<h3>📈 Live Market Scanner</h3>", unsafe_allow_html=True)

    if results:
        df = pd.DataFrame(results)

        # Market summary
        high_count = (df["Type"] == "HIGH MOMENTUM").sum()
        normal_count = (df["Type"] == "NORMAL").sum()

        st.markdown(
            "<div class='card'>"
            f"🔥 High Momentum: {high_count}<br>"
            f"✅ Normal Setups: {normal_count}"
            "</div>",
            unsafe_allow_html=True
        )

        # Row coloring
        def highlight(row):
            if row["Type"] == "HIGH MOMENTUM":
                return ["background-color:#2a1212"] * len(row)
            if row["Type"] == "NORMAL":
                return ["background-color:#102615"] * len(row)
            return [""] * len(row)

        styled_df = df.style.apply(highlight, axis=1)

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=320 if compact else 420
        )
    else:
        st.warning("No high-quality setups right now.")

# ==================================================
# TAB 2 — WATCHLIST (UI READY)
# ==================================================
with tab2:
    st.markdown(
        "<div class='card'>"
        "<b>⭐ Watchlist</b><br>"
        "This section is reserved for manually tracked stocks.<br>"
        "Next step: pin symbols from Scanner."
        "</div>",
        unsafe_allow_html=True
    )

# ==================================================
# TAB 3 — SUMMARY
# ==================================================
with tab3:
    st.markdown(
        "<div class='card'>"
        "<b>📊 Market Summary</b><br>"
        "• Scanner auto-runs every 5 minutes<br>"
        "• Signals are index-aligned<br>"
        "• HIGH MOMENTUM = aggressive trades<br>"
        "• NORMAL = safer intraday trades"
        "</div>",
        unsafe_allow_html=True
    )
