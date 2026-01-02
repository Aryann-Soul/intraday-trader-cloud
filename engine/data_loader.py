import pandas as pd
import requests
from datetime import datetime
import time
import streamlit as st


def _nse_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com"
    })
    session.get("https://www.nseindia.com", timeout=10)
    return session


@st.cache_data(ttl=300)  # cache for 5 minutes
def load_intraday_csv(symbol: str) -> pd.DataFrame:
    """
    Fetch real intraday data from NSE with retries + caching
    """

    if symbol in ["NIFTY", "BANKNIFTY"]:
        url = f"https://www.nseindia.com/api/chart-databyindex?index={symbol}"
    else:
        url = f"https://www.nseindia.com/api/chart-databyindex?index={symbol}%20EQN"

    session = _nse_session()
    last_error = None

    for attempt in range(3):  # smart retry
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                records = []

                for t, o, h, l, c, v in data["grapthData"]:
                    records.append({
                        "datetime": datetime.fromtimestamp(t / 1000),
                        "open": o,
                        "high": h,
                        "low": l,
                        "close": c,
                        "volume": v
                    })

                df = pd.DataFrame(records)
                df.sort_values("datetime", inplace=True)
                return df

        except Exception as e:
            last_error = e
            time.sleep(1)

    # If all retries fail, Streamlit will serve cached data (if available)
    raise RuntimeError("NSE temporary block")
