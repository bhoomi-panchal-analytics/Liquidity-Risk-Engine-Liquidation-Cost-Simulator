

import pandas as pd
import numpy as np

def compute_returns(df: pd.DataFrame):
    df['Returns'] = df['Close'].pct_change()
    return df


def compute_adv(df: pd.DataFrame, window: int = 30):
    df['ADV'] = df['Volume'].rolling(window).mean()
    return df


def compute_volatility(df: pd.DataFrame, window: int = 30):
    df['Volatility'] = df['Returns'].rolling(window).std()
    return df


def compute_spread_proxy(df: pd.DataFrame):
    df['SpreadProxy'] = (df['High'] - df['Low']) / df['Close']
    return df
