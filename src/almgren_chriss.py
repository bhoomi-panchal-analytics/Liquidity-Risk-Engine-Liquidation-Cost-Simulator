# src/almgren_chriss.py

import numpy as np
import pandas as pd

def optimal_execution_schedule(total_shares, days, volatility, eta, risk_aversion):

    kappa = np.sqrt((risk_aversion * volatility**2) / eta)

    t = np.arange(0, days + 1)

    sinh_term = np.sinh(kappa * (days - t)) / np.sinh(kappa * days)

    remaining_shares = total_shares * sinh_term

    trades = -np.diff(remaining_shares)

    schedule = pd.DataFrame({
        "Day": np.arange(1, days + 1),
        "SharesTraded": trades
    })

    return schedule
