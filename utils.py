# src/util.py

import numpy as np
import pandas as pd


# -----------------------------
# Validation Utilities
# -----------------------------

def validate_positive(value, name="Value"):
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    return value


def validate_dataframe_columns(df: pd.DataFrame, required_cols: list):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True


# -----------------------------
# Financial Conversions
# -----------------------------

def compute_dollar_volume(price: float, volume: float):
    return price * volume


def compute_dollar_adv(df: pd.DataFrame):
    df["DollarADV"] = df["Close"] * df["ADV"]
    return df


def shares_from_position_value(position_value: float, price: float):
    validate_positive(price, "Price")
    return position_value / price


def position_value_from_shares(shares: float, price: float):
    return shares * price


# -----------------------------
# Statistical Helpers
# -----------------------------

def annualize_volatility(daily_volatility: float, trading_days: int = 252):
    return daily_volatility * np.sqrt(trading_days)


def percentage(value):
    return value * 100


def compute_percentile(array, percentile):
    return np.percentile(array, percentile)


# -----------------------------
# Risk Metrics Helpers
# -----------------------------

def compute_z_score(confidence_level: float):
    z_map = {
        0.90: 1.28,
        0.95: 1.65,
        0.99: 2.33
    }
    return z_map.get(confidence_level, 1.65)


# -----------------------------
# Execution Helpers
# -----------------------------

def compute_participation_rate(shares_traded: float, adv: float):
    validate_positive(adv, "ADV")
    return shares_traded / adv


def remaining_shares_after_trade(remaining: float, traded: float):
    return max(remaining - traded, 0)
