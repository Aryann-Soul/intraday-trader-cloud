import streamlit as st
from streamlit_autorefresh import st_autorefresh
from engine.scanner import scan_symbols
from datetime import datetime, time as dtime
import pytz
import pandas as pd

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="Intraday Trading Dashboard", layout="wide")

# --------------------------------------------------
# Auto refresh
# --------------------------------------------------
st_autorefresh(interval=300000, key="auto_refresh")

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# --------------------------------------------------
# CSS (safe)
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
# Status bar
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
# Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Scanner", "⭐ Watchlist", "📊 Summary"])

# ==================================================
# TAB 1 — SCANNER
# ==================================================
with tab1:

    # Signal types card
    st.markdown(
        "<div class='card'>"
        "<b>Signal Types</b><br>"
        "🔥 <span class='high'>HIGH MOMENTUM</span> — Fast moves<br>"
        "✅ <span class='normal'>NORMAL</span> — Clean setups"
        "</div>",
        unsafe_allow_html=True
    )

    # Controls (ALWAYS visible)
    col1, col2 = st.columns(2)
    with col1:
        compact = st.toggle("📱 Compact / Pro mode", value=False)
    with col2:
        min_conf = st.slider("🎯 Minimum Confidence", 50, 90, 50, step=5)

    # Market closed banner (NO stop)
    if not is_market_open():
        st.info("Market not active. Scanner runs between 9:20 AM – 3:30 PM IST.")

    NSE_200 = [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
        "SBIN", "ITC", "LT", "AXISBANK", "KOTAKBANK"
    ]

    # Run scanner ONLY if market open
    results = []
    if is_market_open():
        with st.spinner("Scanning market..."):
            results = scan_symbols(NSE_200)

    st.markdown("<h3>📈 Live Market Scanner</h3>", unsafe_allow_html=True)

    if results:
        df = pd.DataFrame(results)
        df = df[df["Confidence"] >= min_conf]

        if df.empty:
            st.warning("No setups match the selected confidence.")
        else:
            # Summary
            high_count = (df["Type"] == "HIGH MOMENTUM").sum()
            normal_count = (df["Type"] == "NORMAL").sum()

            st.markdown(
                "<div class='card'>"
                f"🔥 High Momentum: {high_count}<br>"
                f"✅ Normal Setups: {normal_count}"
                "</div>",
                unsafe_allow_html=True
            )

            # Pin buttons
            for _, row in df.iterrows():
                cols = st.columns([3, 2, 2, 2, 2])
                cols[0].markdown(f"**{row['Symbol']}**")
                cols[1].markdown(row["Signal"])
                cols[2].markdown(row["Type"])
                cols[3].markdown(str(row["Confidence"]))
                if cols[4].button("⭐ Pin", key=f"pin_{row['Symbol']}"):
                    if row["Symbol"] not in st.session_state.watchlist:
                        st.session_state.watchlist.append(row["Symbol"])

            # Row coloring
            def highlight(r):
                if r["Type"] == "HIGH MOMENTUM":
                    return ["background-color:#2a1212"] * len(r)
                if r["Type"] == "NORMAL":
                    return ["background-color:#102615"] * len(r)
                return [""] * len(r)

            st.dataframe(
                df.style.apply(highlight, axis=1),
                use_container_width=True,
                height=320 if compact else 420
            )
    else:
        if is_market_open():
            st.warning("No high-quality setups right now.")

# ==================================================
# TAB 2 — WATCHLIST
# ==================================================
with tab2:
    st.markdown(
        "<div class='card'><b>⭐ Watchlist</b></div>",
        unsafe_allow_html=True
    )

    if not st.session_state.watchlist:
        st.info("No stocks pinned yet.")
    else:
        for sym in st.session_state.watchlist:
            cols = st.columns([4, 2])
            cols[0].markdown(f"**{sym}**")
            if cols[1].button("❌ Remove", key=f"rm_{sym}"):
                st.session_state.watchlist.remove(sym)

# ==================================================
# TAB 3 — SUMMARY
# ==================================================
with tab3:
    st.markdown(
        "<div class='card'>"
        "<b>📊 System Summary</b><br>"
        "• Scanner auto-runs every 5 minutes<br>"
        "• Confidence-based filtering<br>"
        "• Watchlist support<br>"
        "• HIGH MOMENTUM = aggressive trades<br>"
        "• NORMAL = safer trades"
        "</div>",
        unsafe_allow_html=True
    )
