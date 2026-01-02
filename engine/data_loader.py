import pandas as pd
import requests
from io import StringIO

def load_intraday_csv(symbol: str) -> pd.DataFrame:
    """
    TEMPORARY PLACEHOLDER:
    Replace later with real NSE intraday source.
    """

    url = f"https://raw.githubusercontent.com/yourusername/sample-data/main/{symbol}.csv"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Data not available")

    df = pd.read_csv(StringIO(response.text))
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.sort_values("datetime", inplace=True)

    return df
