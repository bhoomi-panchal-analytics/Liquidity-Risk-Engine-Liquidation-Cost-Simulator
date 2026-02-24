import numpy as np
import pandas as pd
from src.liquidation_simulator import simulate_liquidation


def participation_sensitivity(df, total_shares, participation_range, k=1.0):

    results = []

    for pr in participation_range:

        sim = simulate_liquidation(
            df,
            total_shares=total_shares,
            participation_rate=pr,
            k=k
        )

        total_cost = sim["TotalCost"].sum()

        results.append({
            "ParticipationRate": pr,
            "TotalCost": total_cost
        })

    return pd.DataFrame(results)


def stress_scenario(df, vol_multiplier=1.0, adv_multiplier=1.0):

    stressed_df = df.copy()

    stressed_df["Volatility"] *= vol_multiplier
    stressed_df["ADV"] *= adv_multiplier

    return stressed_df
