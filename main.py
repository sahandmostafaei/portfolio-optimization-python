"""
Portfolio Optimization & Asset Allocation
Author: Sahand Mostafaei
"""

import numpy as np
import pandas as pd

from statistics import (
    calculate_returns,
    correlation_matrix,
    covariance_matrix,
)

from optimization import (
    generate_random_portfolios,
    maximum_sharpe_portfolio,
    minimum_risk_portfolio,
)

from visualization import plot_efficient_frontier


def load_sample_data():

    np.random.seed(42)

    prices = pd.DataFrame({
        "AAPL": np.cumprod(1 + np.random.normal(0.0010, 0.0200, 500)) * 100,
        "MSFT": np.cumprod(1 + np.random.normal(0.0008, 0.0180, 500)) * 100,
        "GOOGL": np.cumprod(1 + np.random.normal(0.0012, 0.0220, 500)) * 100,
        "AMZN": np.cumprod(1 + np.random.normal(0.0011, 0.0210, 500)) * 100,
    })

    return prices


def main():

    print("=" * 60)
    print("PORTFOLIO OPTIMIZATION & ASSET ALLOCATION")
    print("=" * 60)

    prices = load_sample_data()

    returns = calculate_returns(prices)

    print("\nDaily Returns")
    print(returns.head())

    print("\nCorrelation Matrix")
    print(correlation_matrix(returns))

    print("\nCovariance Matrix")
    print(covariance_matrix(returns))

    portfolios = generate_random_portfolios(
        returns,
        num_portfolios=5000
    )

    best = maximum_sharpe_portfolio(portfolios)

    safest = minimum_risk_portfolio(portfolios)

    print("\nMaximum Sharpe Portfolio")
    print(f"Expected Return : {best[0]:.3f}")
    print(f"Risk            : {best[1]:.3f}")
    print(f"Sharpe Ratio    : {best[2]:.3f}")

    print("\nMinimum Risk Portfolio")
    print(f"Expected Return : {safest[0]:.3f}")
    print(f"Risk            : {safest[1]:.3f}")
    print(f"Sharpe Ratio    : {safest[2]:.3f}")

    plot_efficient_frontier(portfolios)

    print("\nEfficient frontier saved to figures/efficient_frontier.png")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
