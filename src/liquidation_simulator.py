

import pandas as pd
from src.impact_model import compute_total_cost

def simulate_liquidation(df: pd.DataFrame,
                         total_shares: float,
                         participation_rate: float,
                         k: float = 1.0):

    remaining_shares = total_shares
    results = []

    for index, row in df.iterrows():

        if remaining_shares <= 0:
            break

        daily_adv = row['ADV']
        daily_vol = row['Volatility']
        spread = row['SpreadProxy']
        price = row['Close']

        max_shares_today = participation_rate * daily_adv
        shares_traded = min(remaining_shares, max_shares_today)

        cost_dict = compute_total_cost(
            shares_traded,
            price,
            daily_adv,
            daily_vol,
            spread,
            k
        )

        cost_dict["Date"] = row['Date']
        cost_dict["SharesTraded"] = shares_traded

        results.append(cost_dict)

        remaining_shares -= shares_traded

    return pd.DataFrame(results)
