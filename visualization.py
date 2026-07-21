"""
Visualization Module
Author: Sahand Mostafaei
"""

import os

import matplotlib.pyplot as plt


def create_output_folder():

    os.makedirs("figures", exist_ok=True)


def plot_efficient_frontier(results):

    create_output_folder()

    risks = [p["risk"] for p in results]

    returns = [p["return"] for p in results]

    sharpe = [p["sharpe"] for p in results]

    plt.figure(figsize=(9,6))

    scatter = plt.scatter(
        risks,
        returns,
        c=sharpe,
        s=6
    )

    plt.colorbar(scatter, label="Sharpe Ratio")

    plt.xlabel("Portfolio Risk")

    plt.ylabel("Expected Return")

    plt.title("Efficient Frontier")

    plt.tight_layout()

    plt.savefig("figures/efficient_frontier.png")

    plt.close()
