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

    risks = [r[1] for r in results]

    returns = [r[0] for r in results]

    plt.figure(figsize=(8,6))

    plt.scatter(
        risks,
        returns,
        s=5
    )

    plt.xlabel("Portfolio Risk")

    plt.ylabel("Expected Return")

    plt.title("Efficient Frontier Simulation")

    plt.tight_layout()

    plt.savefig("figures/efficient_frontier.png")

    plt.close()
