# app.py

import streamlit as st
import numpy as np
import pandas as pd

from src.data_loader import fetch_stock_data
from src.data_cleaner import clean_data
from src.metrics import (
    compute_returns,
    compute_adv,
    compute_volatility,
    compute_spread_proxy
)
from src.liquidation_simulator import simulate_liquidation
from src.almgren_chriss import optimal_execution_schedule
from src.monte_carlo import monte_carlo_liquidation_cost


st.set_page_config(page_title="Liquidity Risk Engine", layout="wide")

st.title("Liquidity Risk Engine – Cost of Liquidation Simulator")

# -----------------------------
# Sidebar Inputs
# -----------------------------

st.sidebar.header("Input Parameters")

ticker = st.sidebar.text_input("Stock Ticker", "RELIANCE.NS")
position_size = st.sidebar.number_input("Total Shares to Liquidate", value=500000)

execution_mode = st.sidebar.selectbox(
    "Execution Method",
    ["Participation-Based", "Almgren–Chriss Optimal"]
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

# -----------------------------
# Main Execution Block
# -----------------------------

if run_button:

    try:
        # -------------------------
        # Load and Prepare Data
        # -------------------------

        data = fetch_stock_data(ticker)
        data = clean_data(data)
        data = compute_returns(data)
        data = compute_adv(data)
        data = compute_volatility(data)
        data = compute_spread_proxy(data)

        data = data.dropna()

        if len(data) < 30:
            st.error("Not enough historical data.")
            st.stop()

        # Apply Stress
        data["Volatility"] *= vol_multiplier
        data["ADV"] *= adv_multiplier

        current_price = data["Close"].iloc[-1]
        current_volatility = data["Volatility"].iloc[-1]
        current_adv = data["ADV"].iloc[-1]

        # -------------------------
        # Execution Schedule
        # -------------------------

        if execution_mode == "Participation-Based":

            sim_results = simulate_liquidation(
                data,
                total_shares=position_size,
                participation_rate=participation_rate
            )

            schedule = sim_results[["SharesTraded"]].copy()
            total_cost = sim_results["TotalCost"].sum()
            horizon_days = len(sim_results)

        else:

            horizon_days = 10

            schedule = optimal_execution_schedule(
                total_shares=position_size,
                days=horizon_days,
                volatility=current_volatility,
                eta=1.0,
                risk_aversion=0.01
            )

            # Approximate deterministic cost
            total_cost = 0
            for shares in schedule["SharesTraded"]:
                participation = shares / current_adv
                impact = current_volatility * np.sqrt(participation)
                total_cost += shares * (impact + 0.001 * current_price)

        # -------------------------
        # Monte Carlo Simulation
        # -------------------------

        mc_costs = monte_carlo_liquidation_cost(
            S0=current_price,
            mu=0,
            sigma=current_volatility,
            schedule=schedule,
            simulations=1000
        )

        expected_execution_value = mc_costs.mean()
        worst_5pct = np.percentile(mc_costs, 5)

        # -------------------------
        # Output Section
        # -------------------------

        st.subheader("Execution Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Current Price", f"₹ {round(current_price,2)}")
        col2.metric("Estimated Deterministic Cost", f"₹ {round(total_cost,2)}")
        col3.metric("Liquidation Horizon (Days)", horizon_days)

        st.subheader("Monte Carlo Execution Risk")

        col4, col5 = st.columns(2)

        col4.metric("Expected Execution Value", f"₹ {round(expected_execution_value,2)}")
        col5.metric("5% Worst Outcome", f"₹ {round(worst_5pct,2)}")

        st.subheader("Execution Cost Distribution")
        st.bar_chart(pd.DataFrame(mc_costs))

        st.subheader("Shares Traded per Day")
        st.line_chart(schedule["SharesTraded"])

    except Exception as e:
        st.error(f"Error: {str(e)}")
