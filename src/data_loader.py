import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_multiple_tickers(tickers):

    start = (datetime.today() - timedelta(days=5*365)).strftime("%Y-%m-%d")

    data = yf.download(
        tickers,
        start=start,
        auto_adjust=True,
        progress=False,
        threads=False,
        group_by='ticker'
    )

    cleaned = {}

    for ticker in tickers:
        if ticker in data.columns.levels[0]:
            df = data[ticker].copy()
            df.reset_index(inplace=True)
            cleaned[ticker] = df

    return cleaned
