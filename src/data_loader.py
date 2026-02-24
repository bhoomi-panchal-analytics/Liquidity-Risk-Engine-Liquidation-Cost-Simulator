# src/data_loader.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_last_5y_start():
    return (datetime.today() - timedelta(days=5*365)).strftime("%Y-%m-%d")


def fetch_multiple_tickers(tickers: list):

    start_date = get_last_5y_start()

    data = yf.download(
        tickers,
        start=start_date,
        auto_adjust=True,
        progress=False,
        threads=False,
        group_by='ticker'
    )

    if data.empty:
        raise ValueError("No data fetched from Yahoo.")

    cleaned_data = {}

    for ticker in tickers:
        try:
            df = data[ticker].copy()
            df.reset_index(inplace=True)

            required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]

            if not all(col in df.columns for col in required_cols):
                continue

            df = df.dropna()
            cleaned_data[ticker] = df

        except Exception:
            continue

    if len(cleaned_data) == 0:
        raise ValueError("No valid ticker data found.")

    return cleaned_data
