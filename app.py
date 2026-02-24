# app.py

import streamlit as st
import pandas as pd
import numpy as np

from src.data_loader import fetch_stock_data
from src.data_cleaner import clean_data
from src.metrics import compute_returns, compute_adv, compute_volatility, compute_spread_proxy
from src.liquidation_simulator import simulate_liquidation
from src.sensitivity import participation_sensitivity, stress_scenario

st.title("Liquidity Risk Engine – Cost of Liquidation Simulator")

st.sidebar.header("Input Parameters")

ticker = st.sidebar.text_input("Stock Ticker", "RELIANCE.NS")
position_size = st.sidebar.number_input("Total Shares to Liquidate", value=500000)
participation_rate = st.sidebar.slider("Participation Rate (% of ADV per day)", 1, 50, 10) / 100
vol_multiplier = st.sidebar.slider("Volatility Stress Multiplier", 1.0, 3.0, 1.0)
adv_multiplier = st.sidebar.slider("ADV Stress Multiplier", 0.3, 1.5, 1.0)

if st.sidebar.button("Run Simulation"):

    # Load Data
    data = fetch_stock_data(ticker)
    data = clean_data(data)
    data = compute_returns(data)
    data = compute_adv(data)
    data = compute_volatility(data)
    data = compute_spread_proxy(data)

    data = data.dropna()

    # Apply Stress
    data = stress_scenario(data, vol_multiplier, adv_multiplier)

    # Simulate Liquidation
    sim_results = simulate_liquidation(
        data,
        total_shares=position_size,
        participation_rate=participation_rate
    )

    total_cost = sim_results["TotalCost"].sum()

    st.subheader("Execution Summary")
    st.write(f"Total Liquidation Cost: ₹ {round(total_cost, 2)}")
    st.write(f"Number of Days Required: {len(sim_results)}")

    # Plot Daily Shares
    st.subheader("Daily Shares Traded")
    st.line_chart(sim_results.set_index("Date")["SharesTraded"])

    # Plot Cumulative Cost
    sim_results["CumulativeCost"] = sim_results["TotalCost"].cumsum()
    st.subheader("Cumulative Execution Cost")
    st.line_chart(sim_results.set_index("Date")["CumulativeCost"])

    # Sensitivity Analysis
    st.subheader("Participation Rate Sensitivity")

    pr_range = np.linspace(0.02, 0.30, 10)
    sens_df = participation_sensitivity(data, position_size, pr_range)

    sens_df.set_index("ParticipationRate", inplace=True)
    st.line_chart(sens_df["TotalCost"])
