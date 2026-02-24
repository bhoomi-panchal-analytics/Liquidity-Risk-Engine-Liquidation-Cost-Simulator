import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, start="2018-01-01"):

    try:
        data = yf.download(
            ticker,
            start=start,
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if data is None or data.empty:
            raise ValueError("No data fetched. Check ticker symbol.")

        data.reset_index(inplace=True)
        return data

    except Exception as e:
        raise ValueError(f"Data fetch failed: {str(e)}")
