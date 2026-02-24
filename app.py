# app.py

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.data_loader import fetch_multiple_tickers
from src.data_cleaner import clean_data
from src.metrics import (
    compute_returns,
    compute_adv,
    compute_volatility,
    compute_spread_proxy
)
from src.liquidation_simulator import simulate_liquidation


st.set_page_config(page_title="Liquidity Risk Engine", layout="wide")
st.title("Liquidity Risk Engine – Cost of Liquidation Simulator")


# ----------------------------------------------------
# TICKER UNIVERSE (20 NSE STOCKS)
# ----------------------------------------------------

TICKER_LIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "HINDUNILVR.NS", "ITC.NS", "SBIN.NS",
    "BHARTIARTL.NS", "KOTAKBANK.NS", "LT.NS", "AXISBANK.NS",
    "BAJFINANCE.NS", "MARUTI.NS", "ASIANPAINT.NS",
    "TITAN.NS", "WIPRO.NS", "ULTRACEMCO.NS",
    "SUNPHARMA.NS", "NESTLEIND.NS"
]


# ----------------------------------------------------
# CACHE DATA FETCH
# ----------------------------------------------------

@st.cache_data(show_spinner=True)
def load_data():
    return fetch_multiple_tickers(TICKER_LIST)


try:
    data_dict = load_data()
except Exception as e:
    st.error(f"Data Fetch Failed: {str(e)}")
    st.stop()


# ----------------------------------------------------
# SIDEBAR INPUTS
# ----------------------------------------------------

st.sidebar.header("Input Parameters")

selected_ticker = st.sidebar.selectbox(
    "Select Stock",
    list(data_dict.keys())
)

position_size = st.sidebar.number_input(
    "Total Shares to Liquidate",
    value=500000
)

participation_rate = st.sidebar.slider(
    "Participation Rate (% of ADV per day)",
    1, 50, 10
) / 100

vol_multiplier = st.sidebar.slider(
    "Volatility Stress Multiplier",
    1.0, 3.0, 1.0
)

adv_multiplier = st.sidebar.slider(
    "ADV Stress Multiplier",
    0.3, 1.5, 1.0
)

run_button = st.sidebar.button("Run Simulation")


# ----------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------

if run_button:

    try:
        data = data_dict[selected_ticker].copy()

        # Clean & Compute Metrics
        data = clean_data(data)
        data = compute_returns(data)
        data = compute_adv(data)
        data = compute_volatility(data)
        data = compute_spread_proxy(data)

        data = data.dropna()

        if len(data) < 30:
            st.error("Insufficient processed data.")
            st.stop()

        # Apply stress
        data["Volatility"] *= vol_multiplier
        data["ADV"] *= adv_multiplier

        current_price = data["Close"].iloc[-1]
        current_volatility = data["Volatility"].iloc[-1]
        current_adv = data["ADV"].iloc[-1]

        # Liquidation Simulation
        sim_results = simulate_liquidation(
            data,
            total_shares=position_size,
            participation_rate=participation_rate
        )

        total_cost = sim_results["TotalCost"].sum()
        horizon_days = len(sim_results)

        # ------------------------------------------------
        # OUTPUT
        # ------------------------------------------------

        st.subheader("Execution Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Current Price", f"₹ {round(current_price,2)}")
        col2.metric("Estimated Liquidation Cost", f"₹ {round(total_cost,2)}")
        col3.metric("Liquidation Horizon (Days)", horizon_days)

        st.subheader("Shares Traded Per Day")
        st.line_chart(sim_results.set_index("Date")["SharesTraded"])

        sim_results["CumulativeCost"] = sim_results["TotalCost"].cumsum()

        st.subheader("Cumulative Execution Cost")
        st.line_chart(sim_results.set_index("Date")["CumulativeCost"])

    except Exception as e:
        st.error(f"Execution Failed: {str(e)}")
