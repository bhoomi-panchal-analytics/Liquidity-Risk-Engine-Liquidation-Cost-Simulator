# app.py

import streamlit as st
import pandas as pd
import numpy as np

from data_loader import fetch_multiple_tickers
from data_cleaner import clean_data
from metrics import compute_returns, compute_adv, compute_volatility, compute_spread_proxy
from liquidation_simulator import simulate_liquidation
from monte_carlo import monte_carlo_liquidation_cost


st.set_page_config(layout="wide")
st.title("Liquidity Risk Engine – Institutional Dashboard")


# -----------------------------
# Ticker Universe
# -----------------------------

TICKERS = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "HINDUNILVR.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS",
    "LT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","ASIANPAINT.NS",
    "TITAN.NS","WIPRO.NS","ULTRACEMCO.NS","SUNPHARMA.NS","NESTLEIND.NS"
]


@st.cache_data
def load_data():
    return fetch_multiple_tickers(TICKERS)


data_dict = load_data()


# -----------------------------
# Sidebar Controls
# -----------------------------

selected = st.sidebar.selectbox("Select Stock", list(data_dict.keys()))
position_size = st.sidebar.number_input("Position Size", value=500000)
participation = st.sidebar.slider("Participation %", 1, 50, 10) / 100
vol_stress = st.sidebar.slider("Volatility Stress", 1.0, 3.0, 1.0)
adv_stress = st.sidebar.slider("ADV Stress", 0.3, 1.5, 1.0)
simulations = st.sidebar.slider("Monte Carlo Simulations", 100, 2000, 1000)

run = st.sidebar.button("Run Simulation")


if run:

    data = data_dict[selected].copy()
    data = clean_data(data)
    data = compute_returns(data)
    data = compute_adv(data)
    data = compute_volatility(data)
    data = compute_spread_proxy(data)
    data = data.dropna()

    data["Volatility"] *= vol_stress
    data["ADV"] *= adv_stress

    current_price = data["Close"].iloc[-1]
    current_vol = data["Volatility"].iloc[-1]
    current_adv = data["ADV"].iloc[-1]

    sim_results = simulate_liquidation(data, position_size, participation)

    if sim_results.empty:
        st.warning("No liquidation executed. Increase participation.")
        st.stop()

    total_cost = sim_results["TotalCost"].sum()

    mc_costs = monte_carlo_liquidation_cost(
        S0=current_price,
        mu=0,
        sigma=current_vol,
        schedule=sim_results[["SharesTraded"]],
        simulations=simulations
    )

    # ---------------- Metrics ----------------

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", round(current_price,2))
    col2.metric("Total Liquidation Cost", round(total_cost,2))
    col3.metric("Execution Days", len(sim_results))

    st.markdown("---")

    # ---------------- Visualization 1 ----------------
    st.subheader("1. Daily Shares Traded")
    st.line_chart(sim_results["SharesTraded"])

    # ---------------- Visualization 2 ----------------
    st.subheader("2. Cumulative Cost")
    cumulative = sim_results["TotalCost"].cumsum()
    st.line_chart(cumulative)

    # ---------------- Visualization 3 ----------------
    st.subheader("3. Monte Carlo Distribution")
    st.bar_chart(pd.Series(mc_costs).value_counts().sort_index())

    # ---------------- Visualization 4 ----------------
    st.subheader("4. Participation Sensitivity")

    participation_range = np.linspace(0.05, 0.40, 8)
    costs = []

    for pr in participation_range:
        sim = simulate_liquidation(data, position_size, pr)
        costs.append(sim["TotalCost"].sum())

    sensitivity_df = pd.DataFrame({
        "Participation": participation_range,
        "Cost": costs
    })

    st.line_chart(sensitivity_df.set_index("Participation"))

    # ---------------- Visualization 5 ----------------
    st.subheader("5. Liquidity Pressure (Position vs ADV)")
    pressure_df = pd.DataFrame({
        "Metric": ["ADV", "Position Size"],
        "Value": [current_adv, position_size]
    }).set_index("Metric")

    st.bar_chart(pressure_df)

    # ---------------- Interpretation ----------------

    st.markdown("### Interpretation")
    st.write("""
    1. Daily Shares Traded reflects execution pacing.
    2. Cumulative Cost shows convex cost growth.
    3. Monte Carlo Distribution exposes tail execution risk.
    4. Participation Sensitivity demonstrates nonlinear impact.
    5. Liquidity Pressure compares position to market depth.
    """)
