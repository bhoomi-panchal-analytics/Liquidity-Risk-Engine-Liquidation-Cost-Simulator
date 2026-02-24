# src/visualization.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_shares_traded(sim_results):
    fig, ax = plt.subplots()
    ax.plot(sim_results["Date"], sim_results["SharesTraded"])
    ax.set_title("Daily Shares Traded")
    ax.set_xlabel("Date")
    ax.set_ylabel("Shares")
    return fig


def plot_cumulative_cost(sim_results):
    sim_results["CumulativeCost"] = sim_results["TotalCost"].cumsum()
    fig, ax = plt.subplots()
    ax.plot(sim_results["Date"], sim_results["CumulativeCost"])
    ax.set_title("Cumulative Execution Cost")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cost")
    return fig


def plot_cost_distribution(mc_costs):
    fig, ax = plt.subplots()
    ax.hist(mc_costs, bins=30)
    ax.set_title("Monte Carlo Cost Distribution")
    ax.set_xlabel("Execution Value")
    ax.set_ylabel("Frequency")
    return fig


def plot_participation_sensitivity(df, position_size, simulate_func):
    participation_range = np.linspace(0.05, 0.40, 8)
    costs = []

    for pr in participation_range:
        sim = simulate_func(df, position_size, pr)
        costs.append(sim["TotalCost"].sum())

    fig, ax = plt.subplots()
    ax.plot(participation_range, costs)
    ax.set_title("Cost vs Participation Rate")
    ax.set_xlabel("Participation Rate")
    ax.set_ylabel("Total Cost")
    return fig


def plot_adv_vs_position(current_adv, position_size):
    fig, ax = plt.subplots()
    ax.bar(["ADV", "Position Size"], [current_adv, position_size])
    ax.set_title("Position Size vs ADV")
    return fig
