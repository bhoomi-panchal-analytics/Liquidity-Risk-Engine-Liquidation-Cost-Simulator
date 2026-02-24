# Liquidity-Risk-Engine-Liquidation-Cost-Simulator

_
This project builds a quantitative model to estimate the cost of liquidating a large equity position under realistic market liquidity constraints. The model incorporates average daily trading volume (ADV), bid-ask spread, and volume participation rates to simulate slippage, spread cost, and temporary market impact. It provides a numerical framework to evaluate liquidity risk and optimal liquidation schedules._

Objective
To develop a quantitative framework that:

Estimates liquidation cost as a function of position size relative to ADV.

Quantifies spread cost and temporary market impact.

Simulates execution under different participation rates (e.g., 5%, 10%, 20% of ADV).

Provides a visualization interface using Streamlit to interactively assess liquidity risk.

Problem Statement
Institutional investors often hold positions large relative to market liquidity. Forced liquidation due to margin calls, risk limits, or redemptions can significantly impact execution prices. Traditional mark-to-market valuation ignores execution cost.

This project aims to answer:

What is the expected cost of liquidating a large stock position over a fixed horizon, given constraints on daily trading volume and prevailing bid-ask spreads?

Model Framework

We decompose total liquidation cost into:

Spread Cost
Spread Cost ≈ (Bid-Ask Spread / 2) × Shares

Temporary Market Impact
Use square-root impact model:

Impact ≈ σ × √(Q / ADV)

where:
σ = daily volatility
Q = shares traded
ADV = average daily volume

Participation Constraint
Daily traded volume ≤ Participation Rate × ADV

Total Execution Cost
Total Cost = Spread Cost + Temporary Impact Cost

Advanced extension (optional):
Implement simplified Almgren–Chriss model with risk-aversion parameter.

Data Needed

For each stock:

• Historical daily price data (Close, High, Low)
• Daily trading volume
• Bid-Ask spread (if unavailable, approximate using high-low or fixed basis points)
• Daily volatility (computed from returns)

Data sources:
• Yahoo Finance (yfinance)
• NSE/BSE data
• Quandl (if available)

Input parameters (user-defined):

• Position size (shares or % of ADV)
• Liquidation horizon (days)
• Participation rate (%)
• Risk aversion parameter (optional)

Files to be Created

Project Structure:

liquidity-risk-engine/
│
├── data/
│ └── raw_data.csv
│
├── src/
│ ├── data_loader.py
│ ├── metrics.py
│ ├── impact_model.py
│ ├── liquidation_simulator.py
│ └── utils.py
│
├── notebooks/
│ └── exploratory_analysis.ipynb
│
├── app.py (Streamlit App)
├── requirements.txt
└── README.md

File Responsibilities

data_loader.py
Fetch historical prices and volumes using yfinance.

metrics.py
Compute:
• ADV
• Volatility
• Spread proxy
• Participation rate

impact_model.py
Implement:
• Spread cost
• Square-root impact function
• Cost per share

liquidation_simulator.py
Simulate daily liquidation schedule and cumulative cost.

app.py
Interactive Streamlit dashboard.

Streamlit App Features

Inputs (sidebar):
• Stock ticker
• Position size
• Participation rate
• Liquidation days

Outputs:
• ADV and volatility
• Total liquidation cost (₹ and %)
• Daily liquidation schedule chart
• Cost vs participation rate graph
• Cost vs liquidation horizon graph

Visualizations:
• Bar chart of daily execution
• Line chart of cumulative cost
• Sensitivity analysis plots
