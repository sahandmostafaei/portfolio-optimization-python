"""
Portfolio Optimization & Asset Allocation
Author: Sahand Mostafaei
"""

import yfinance as yf

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


TICKERS = [
    "AAPL",
    "MSFT",
    "AMZN",
    "GOOGL",
]


def load_market_data():

    print("Downloading historical market data...")

    prices = yf.download(
        TICKERS,
        start="2020-01-01",
        end="2025-01-01"
    )["Close"]

    return prices


def print_portfolio(title, portfolio):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"Expected Return : {portfolio['return']:.3f}")
    print(f"Portfolio Risk  : {portfolio['risk']:.3f}")
    print(f"Sharpe Ratio    : {portfolio['sharpe']:.3f}")
    print(f"Sortino Ratio   : {portfolio['sortino']:.3f}")

    print("\nPortfolio Allocation")

    for ticker, weight in zip(TICKERS, portfolio["weights"]):
        print(f"{ticker:6} : {weight*100:.2f}%")


def main():

    print("=" * 60)
    print("PORTFOLIO OPTIMIZATION & ASSET ALLOCATION")
    print("=" * 60)

    prices = load_market_data()

    returns = calculate_returns(prices)

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

    print_portfolio(
        "MAXIMUM SHARPE PORTFOLIO",
        best
    )

    print_portfolio(
        "MINIMUM RISK PORTFOLIO",
        safest
    )

    plot_efficient_frontier(portfolios)

    print("\nEfficient frontier saved to figures/efficient_frontier.png")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
