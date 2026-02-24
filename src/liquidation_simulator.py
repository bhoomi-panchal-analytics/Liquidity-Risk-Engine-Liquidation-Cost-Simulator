# liquidation_simulator.py

import pandas as pd
import numpy as np


def simulate_liquidation(df, total_shares, participation_rate):

    remaining = total_shares
    results = []

    for _, row in df.iterrows():

        if remaining <= 0:
            break

        adv = row["ADV"]
        vol = row["Volatility"]
        spread = row["SpreadProxy"]
        price = row["Close"]

        if pd.isna(adv) or adv <= 0:
            continue

        max_trade = participation_rate * adv
        trade = min(remaining, max_trade)

        if trade <= 0:
            continue

        impact = vol * np.sqrt(trade / adv)
        spread_cost = spread * price * 0.5

        total_cost = trade * (impact + spread_cost)

        results.append({
            "SharesTraded": trade,
            "TotalCost": total_cost
        })

        remaining -= trade

    return pd.DataFrame(results)
