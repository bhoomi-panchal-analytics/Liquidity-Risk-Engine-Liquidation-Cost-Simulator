# Liquidity-Risk-Engine-Liquidation-Cost-Simulator

_
This project builds a quantitative model to estimate the cost of liquidating a large equity position under realistic market liquidity constraints. The model incorporates average daily trading volume (ADV), bid-ask spread, and volume participation rates to simulate slippage, spread cost, and temporary market impact. It provides a numerical framework to evaluate liquidity risk and optimal liquidation schedules._

**Objective**
To develop a quantitative framework that:

Estimates liquidation cost as a function of position size relative to ADV.

Quantifies spread cost and temporary market impact.

Simulates execution under different participation rates (e.g., 5%, 10%, 20% of ADV).

Provides a visualization interface using Streamlit to interactively assess liquidity risk.

**Problem Statement**

Institutional investors often hold positions large relative to market liquidity. Forced liquidation due to margin calls, risk limits, or redemptions can significantly impact execution prices. Traditional mark-to-market valuation ignores execution cost.

**This project aims to answer:** 

What is the expected cost of liquidating a large stock position over a fixed horizon, given constraints on daily trading volume and prevailing bid-ask spreads?

Model Framework

We decompose total liquidation cost into:

Spread Cost
Spread Cost ≈ (Bid-Ask Spread / 2) × Shares

## Temporary Market Impact
**Use square-root impact model:**

Impact ≈ σ × √(Q / ADV)


where:

σ = daily volatility

Q = shares traded

ADV = average daily volume


Participation Constraint

Daily traded volume ≤ Participation Rate × ADV


Total Execution Cost

Total Cost = Spread Cost + Temporary Impact Cost


**Advanced extension (optional):**

Implement simplified Almgren–Chriss model with risk-aversion parameter.

Data Needed


**For each stock:**

• Historical daily price data (Close, High, Low)

• Daily trading volume

• Bid-Ask spread (if unavailable, approximate using high-low or fixed basis points)

• Daily volatility (computed from returns)



**Data sources:**

• Yahoo Finance (yfinance)

• NSE/BSE data

• Quandl (if available)


**Input parameters (user-defined):**

• Position size (shares or % of ADV)

• Liquidation horizon (days)

• Participation rate (%)

• Risk aversion parameter (optional)

Files to be Created


### **Project Structure:**

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

**File Responsibilities**

data_loader.py : Fetch historical prices and volumes using yfinance.

**metrics.py
Compute:**

• ADV

• Volatility

• Spread proxy

• Participation rate



**impact_model.py
Implement:**

• Spread cost

• Square-root impact function

• Cost per share

**liquidation_simulator.py** 
Simulate daily liquidation schedule and cumulative cost.

**app.py**
Interactive Streamlit dashboard.

Streamlit App Features

**Inputs (sidebar):** 

• Stock ticker

• Position size

• Participation rate

• Liquidation days


**Outputs:**

• ADV and volatility

• Total liquidation cost (₹ and %)

• Daily liquidation schedule chart

• Cost vs participation rate graph

• Cost vs liquidation horizon graph


**Visualizations:**

• Bar chart of daily execution

• Line chart of cumulative cost

• Sensitivity analysis plots


## Motivation

Traditional valuation assumes positions can be liquidated at current market prices. This assumption fails for large institutional holdings.

Execution introduces:

* Bid-ask spread costs
* Temporary market impact
* Permanent price impact
* Timing risk due to volatility
* Liquidity regime dependence

This project models these effects explicitly.

---

## Problem Statement

Given:

* A large stock position
* Average Daily Volume (ADV)
* Bid-Ask spread
* Daily volatility

Estimate:

1. Expected liquidation cost
2. Optimal execution trajectory
3. Stress-adjusted execution cost
4. Liquidity-adjusted Value-at-Risk

---

## Mathematical Framework

### 1. Temporary Market Impact (Square-Root Model)

Empirical evidence suggests market impact scales sub-linearly:

Impact per share ∝ σ √(Q / ADV)

Where:

* Q = shares traded
* ADV = average daily volume
* σ = daily volatility

Total impact cost:

Impact Cost = Q × k σ √(Q / ADV)

k = impact coefficient

---

### 2. Spread Cost

Spread Cost ≈ (Bid-Ask Spread / 2) × Shares

---

### 3. Total Execution Cost

Total Cost = Spread Cost + Temporary Impact Cost

---

### 4. Optimal Execution (Almgren–Chriss Model)

Minimize:

E(Cost) + λ Var(Cost)

Where:

* λ = risk aversion parameter
* Higher λ → faster execution
* Lower λ → slower execution

Closed-form optimal trajectory:

x(t) = X₀ sinh(κ(T − t)) / sinh(κT)

Where:

κ² = (λ σ²) / η

η = temporary impact parameter

---

### 5. Monte Carlo Simulation

Price evolution modeled via Geometric Brownian Motion:

S(t+1) = S(t) exp[(μ − 0.5σ²)Δt + σ√Δt ε]

This enables:

* Distribution of execution outcomes
* Expected liquidation value
* Worst-case execution scenarios

---

### 6. Liquidity-Adjusted Value-at-Risk (L-VaR)

Traditional VaR:

VaR = z σ √T × Position Value

Liquidity-Adjusted VaR:

L-VaR = Market VaR + Expected Liquidation Cost

This captures execution friction in downside risk.

---

## Project Structure

```
liquidity-risk-engine/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── metrics.py
│   ├── impact_model.py
│   ├── liquidation_simulator.py
│   ├── almgren_chriss.py
│   ├── sensitivity.py
│   ├── liquidity_var.py
│   ├── monte_carlo.py
│   └── logger.py
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Features

* Rolling ADV and volatility computation
* Participation-rate constrained liquidation
* Stress scenarios (volatility ↑, ADV ↓)
* Optimal execution schedule
* Monte Carlo execution risk simulation
* Liquidity-adjusted VaR computation
* Interactive Streamlit dashboard

---

## Streamlit Dashboard

The interface allows:

* Ticker selection
* Position size input
* Participation rate adjustment
* Volatility & liquidity stress toggles
* Visualization of liquidation schedule
* Sensitivity analysis
* Execution risk distribution

Run with:

```
pip install -r requirements.txt
streamlit run app.py
```

---

## Stress Testing

Crisis simulation allows:

* Volatility multiplier
* ADV contraction
* Spread widening

Liquidity risk increases convexly under stress.

---

## Key Insights

* Execution cost grows non-linearly with participation rate
* Liquidity risk is regime-dependent
* Volatility amplifies impact
* Optimal execution balances impact vs timing risk
* Liquidity-adjusted VaR captures hidden downside exposure

---

## Limitations

* Constant volatility assumption
* No intraday modeling
* No limit order book depth modeling
* Impact coefficients not empirically calibrated
* No regime-switching volatility

Future improvements may include:

* GARCH volatility modeling
* Markov regime-switch model
* Order book depth modeling
* Empirical calibration using trade-level data

---

## Applications

* Portfolio risk management
* Block trade execution planning
* Liquidity stress testing
* Hedge fund risk analysis
* Institutional execution research

---

## Author Positioning

This project demonstrates:

* Market microstructure understanding
  
* Execution cost modeling
  
* Risk-adjusted optimization
* Quantitative simulation techniques
* Financial risk engineering

---
