# src/impact_model.py

import numpy as np

def compute_spread_cost(spread_proxy: float, shares: float, price: float):
    """
    Spread cost approximation.
    spread_proxy assumed as percentage (e.g. 0.01 = 1%)
    """
    spread_per_share = spread_proxy * price
    return (spread_per_share / 2) * shares


def compute_temporary_impact(shares: float, adv: float, volatility: float, k: float = 1.0):
    """
    Square-root impact model.
    """
    participation_rate = shares / adv
    impact_per_share = k * volatility * np.sqrt(participation_rate)
    return impact_per_share


def compute_total_cost(shares: float, price: float, adv: float,
                       volatility: float, spread_proxy: float,
                       k: float = 1.0):

    spread_cost = compute_spread_cost(spread_proxy, shares, price)

    impact_per_share = compute_temporary_impact(
        shares, adv, volatility, k
    )

    impact_cost = impact_per_share * shares

    total_cost = spread_cost + impact_cost

    return {
        "SpreadCost": spread_cost,
        "ImpactCost": impact_cost,
        "TotalCost": total_cost,
        "ParticipationRate": shares / adv
    }
