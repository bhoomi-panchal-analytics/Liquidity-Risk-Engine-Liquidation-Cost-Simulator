

import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker: str, start: str = "2018-01-01", end: str = None):
    """
    Fetch historical OHLCV data from Yahoo Finance.
    """

    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise ValueError("No data fetched. Check ticker symbol.")

    data.reset_index(inplace=True)

    # Ensure required columns exist
    required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing column: {col}")

    return data


def save_raw_data(data: pd.DataFrame, ticker: str):
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/{ticker}_raw.csv"
    data.to_csv(file_path, index=False)
    return file_path
