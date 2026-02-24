# src/liquidation_simulator.py

import pandas as pd
from src.impact_model import compute_total_cost


def simulate_liquidation(df, total_shares, participation_rate):

    remaining_shares = total_shares
    results = []

    for _, row in df.iterrows():

        if remaining_shares <= 0:
            break

        daily_adv = row.get("ADV", 0)
        daily_vol = row.get("Volatility", 0)
        spread = row.get("SpreadProxy", 0)
        price = row.get("Close", 0)
        date = row.get("Date", None)

        if pd.isna(daily_adv) or daily_adv <= 0:
            continue

        max_shares_today = participation_rate * daily_adv
        shares_traded = min(remaining_shares, max_shares_today)

        if shares_traded <= 0:
            continue

        cost_dict = compute_total_cost(
            shares_traded,
            price,
            daily_adv,
            daily_vol,
            spread
        )

        cost_dict["Date"] = date
        cost_dict["SharesTraded"] = shares_traded

        results.append(cost_dict)

        remaining_shares -= shares_traded

    if len(results) == 0:
        return pd.DataFrame(columns=["Date", "SharesTraded", "TotalCost"])

    return pd.DataFrame(results)
