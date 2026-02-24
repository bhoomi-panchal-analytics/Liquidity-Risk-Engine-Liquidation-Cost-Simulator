# src/visualization.py

import matplotlib.pyplot as plt
import numpy as np


def plot_shares_traded(sim_results):

    fig, ax = plt.subplots()

    days = range(1, len(sim_results) + 1)
    ax.plot(days, sim_results["SharesTraded"].values)

    ax.set_title("Daily Shares Traded (Execution Horizon)")
    ax.set_xlabel("Execution Day")
    ax.set_ylabel("Shares Traded")

    return fig


def plot_cumulative_cost(sim_results):

    cumulative = sim_results["TotalCost"].cumsum().values
    days = range(1, len(sim_results) + 1)

    fig, ax = plt.subplots()
    ax.plot(days, cumulative)

    ax.set_title("Cumulative Execution Cost")
    ax.set_xlabel("Execution Day")
    ax.set_ylabel("Cost")

    return fig


def plot_cost_distribution(mc_costs):

    fig, ax = plt.subplots()
    ax.hist(mc_costs, bins=40)

    ax.set_title("Monte Carlo Execution Value Distribution")
    ax.set_xlabel("Execution Value")
    ax.set_ylabel("Frequency")

    return fig


def plot_participation_sensitivity(sim_func, data, position_size):

    participation_range = np.linspace(0.05, 0.40, 10)
    costs = []

    for pr in participation_range:
        sim = sim_func(data, position_size, pr)
        costs.append(sim["TotalCost"].sum())

    fig, ax = plt.subplots()
    ax.plot(participation_range, costs)

    ax.set_title("Cost vs Participation Rate")
    ax.set_xlabel("Participation Rate")
    ax.set_ylabel("Total Cost")

    return fig


def plot_adv_pressure(current_adv, position_size):

    fig, ax = plt.subplots()

    ax.bar(["ADV", "Position Size"], [current_adv, position_size])

    ax.set_title("Liquidity Pressure: Position vs ADV")

    return fig
