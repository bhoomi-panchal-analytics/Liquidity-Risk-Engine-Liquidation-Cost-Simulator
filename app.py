# app.py

import streamlit as st
import numpy as np
import pandas as pd

from src.data_loader import fetch_multiple_tickers
from src.data_cleaner import clean_data
from src.metrics import compute_returns, compute_adv, compute_volatility, compute_spread_proxy
from src.liquidation_simulator import simulate_liquidation
from src.monte_carlo import monte_carlo_liquidation_cost
from src.visualization import (
    plot_shares_traded,
    plot_cumulative_cost,
    plot_cost_distribution,
    plot_participation_sensitivity,
    plot_adv_vs_position
)

st.set_page_config(layout="wide")
st.title("Liquidity Risk Engine – Institutional Dashboard")


# ----------------------------
# Sidebar Controls
# ----------------------------

TICKER_LIST = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "HINDUNILVR.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS",
    "LT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","ASIANPAINT.NS",
    "TITAN.NS","WIPRO.NS","ULTRACEMCO.NS","SUNPHARMA.NS","NESTLEIND.NS"
]

@st.cache_data
def load_data():
    return fetch_multiple_tickers(TICKER_LIST)

data_dict = load_data()

selected_ticker = st.sidebar.selectbox("Select Stock", list(data_dict.keys()))
position_size = st.sidebar.number_input("Position Size", value=500000)
participation_rate = st.sidebar.slider("Participation %", 1, 50, 10)/100
vol_multiplier = st.sidebar.slider("Volatility Stress", 1.0, 3.0, 1.0)
adv_multiplier = st.sidebar.slider("ADV Stress", 0.3, 1.5, 1.0)
simulations = st.sidebar.slider("Monte Carlo Simulations", 100, 3000, 1000)

run_button = st.sidebar.button("Run Simulation")


if run_button:

    data = data_dict[selected_ticker].copy()
    data = clean_data(data)
    data = compute_returns(data)
    data = compute_adv(data)
    data = compute_volatility(data)
    data = compute_spread_proxy(data)
    data = data.dropna()

    data["Volatility"] *= vol_multiplier
    data["ADV"] *= adv_multiplier

    current_price = data["Close"].iloc[-1]
    current_volatility = data["Volatility"].iloc[-1]
    current_adv = data["ADV"].iloc[-1]

    sim_results = simulate_liquidation(
        data,
        total_shares=position_size,
        participation_rate=participation_rate
    )

    if sim_results.empty:
        st.warning("No liquidation executed. Increase participation rate.")
        st.stop()

    total_cost = sim_results["TotalCost"].sum()

    mc_costs = monte_carlo_liquidation_cost(
        S0=current_price,
        mu=0,
        sigma=current_volatility,
        schedule=sim_results[["SharesTraded"]],
        simulations=simulations
    )

    # ---------------- Metrics Section ----------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", round(current_price,2))
    col2.metric("Total Liquidation Cost", round(total_cost,2))
    col3.metric("Horizon (Days)", len(sim_results))

    st.markdown("---")

    # ---------------- Visualizations ----------------

    colA, colB = st.columns(2)
    colA.pyplot(plot_shares_traded(sim_results))
    colB.pyplot(plot_cumulative_cost(sim_results))

    colC, colD = st.columns(2)
    colC.pyplot(plot_cost_distribution(mc_costs))
    colD.pyplot(plot_participation_sensitivity(data, position_size, simulate_liquidation))

    st.pyplot(plot_adv_vs_position(current_adv, position_size))

    # ---------------- Interpretation ----------------

    st.markdown("### Interpretation")
    st.write("""
    1. **Daily Shares Traded** shows execution pacing under participation constraints.  
    2. **Cumulative Cost** highlights convex growth in execution friction.  
    3. **Monte Carlo Distribution** reveals tail execution risk.  
    4. **Participation Sensitivity** demonstrates non-linear cost scaling.  
    5. **Position vs ADV** indicates liquidity pressure relative to market depth.  
    """)
