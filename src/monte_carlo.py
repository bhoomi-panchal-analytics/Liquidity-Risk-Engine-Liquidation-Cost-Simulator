# src/monte_carlo.py

import numpy as np
import pandas as pd

def simulate_price_paths(S0, mu, sigma, days, simulations=1000):

    dt = 1
    paths = np.zeros((days + 1, simulations))
    paths[0] = S0

    for t in range(1, days + 1):
        epsilon = np.random.normal(0, 1, simulations)
        paths[t] = paths[t-1] * np.exp(
            (mu - 0.5 * sigma**2) * dt +
            sigma * np.sqrt(dt) * epsilon
        )

    return paths
