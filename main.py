"""
Portfolio Optimization Analysis

This script:
1. Downloads historical adjusted closing prices for a diversified ETF universe.
2. Calculates historical annualized returns and covariance.
3. Generates random portfolio weights using Monte Carlo simulation.
4. Calculates portfolio return, volatility, Sharpe ratio, and Sortino ratio.
5. Identifies the maximum-Sharpe and minimum-volatility portfolios.
6. Visualizes the simulated portfolio opportunity set.

Note:
Monte Carlo simulation provides an approximate opportunity set. It does not
constitute a formal constrained optimization algorithm.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from optimization import (
    calculate_portfolio_metrics,
    generate_random_weights,
)


# ============================================================
# Configuration
# ============================================================

TICKERS = [
    "SPY",   # US equities
    "EFA",   # Developed-market equities
    "EEM",   # Emerging-market equities
    "TLT",   # Long-term US Treasuries
    "GLD",   # Gold
    "DBC",   # Broad commodities
    "VNQ",   # US real estate
]

START_DATE = "2020-01-01"
END_DATE = "2025-01-01"

NUM_PORTFOLIOS = 5000
RISK_FREE_RATE = 0.0
TRADING_DAYS = 252
RANDOM_SEED = 42


# ============================================================
# Data Download
# ============================================================

def download_price_data(tickers, start_date, end_date):
    """
    Download historical adjusted closing prices.

    Parameters
    ----------
    tickers : list
        List of ticker symbols.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.

    Returns
    -------
    pandas.DataFrame
        Adjusted closing prices.
    """

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(
            "No market data was downloaded. "
            "Check the ticker symbols and internet connection."
        )

    # yfinance may return a MultiIndex when downloading multiple securities.
    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.get_level_values(0):
            prices = data["Close"]
        else:
            prices = data.xs("Close", axis=1, level=0)
    else:
        prices = data[["Close"]]

    prices = prices.dropna(how="all")
    prices = prices.dropna(axis=1, how="all")

    missing_tickers = [
        ticker for ticker in tickers
        if ticker not in prices.columns
    ]

    if missing_tickers:
        raise ValueError(
            f"Missing market data for: {missing_tickers}"
        )

    prices = prices[tickers].dropna()

    if prices.empty:
        raise ValueError(
            "No complete observations remain after removing missing values."
        )

    return prices


# ============================================================
# Portfolio Simulation
# ============================================================

def simulate_portfolios(
    returns,
    num_portfolios,
    risk_free_rate,
    trading_days,
    seed,
):
    """
    Generate random portfolios and calculate their performance metrics.

    Returns
    -------
    pandas.DataFrame
        Portfolio-level simulation results.
    """

    rng = np.random.default_rng(seed)

    num_assets = len(returns.columns)

    mean_returns = returns.mean() * trading_days
    covariance_matrix = returns.cov() * trading_days

    portfolio_results = []

    for portfolio_id in range(num_portfolios):

        weights = generate_random_weights(
            num_assets=num_assets,
            rng=rng,
        )

        portfolio_return, portfolio_volatility, sharpe_ratio, sortino_ratio = (
            calculate_portfolio_metrics(
                weights=weights,
                mean_returns=mean_returns,
                covariance_matrix=covariance_matrix,
                returns=returns,
                risk_free_rate=risk_free_rate,
                trading_days=trading_days,
            )
        )

        portfolio_results.append(
            {
                "portfolio_id": portfolio_id,
                "return": portfolio_return,
                "volatility": portfolio_volatility,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                **{
                    ticker: weight
                    for ticker, weight in zip(
                        returns.columns,
                        weights,
                    )
                },
            }
        )

    return pd.DataFrame(portfolio_results)


# ============================================================
# Portfolio Selection
# ============================================================

def identify_key_portfolios(results):
    """
    Identify the maximum-Sharpe and minimum-volatility portfolios.
    """

    max_sharpe_index = results["sharpe_ratio"].idxmax()
    min_volatility_index = results["volatility"].idxmin()

    max_sharpe_portfolio = results.loc[max_sharpe_index]
    min_volatility_portfolio = results.loc[min_volatility_index]

    return max_sharpe_portfolio, min_volatility_portfolio


# ============================================================
# Reporting
# ============================================================

def print_portfolio_summary(
    portfolio,
    title,
    tickers,
):
    """
    Print portfolio performance and asset weights.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"Expected annual return: {portfolio['return']:.2%}")
    print(f"Annual volatility:      {portfolio['volatility']:.2%}")
    print(f"Sharpe ratio:            {portfolio['sharpe_ratio']:.3f}")
    print(f"Sortino ratio:           {portfolio['sortino_ratio']:.3f}")

    print("\nPortfolio weights:")

    for ticker in tickers:
        print(f"  {ticker}: {portfolio[ticker]:.2%}")


# ============================================================
# Visualization
# ============================================================

def plot_portfolio_opportunity_set(
    results,
    max_sharpe_portfolio,
    min_volatility_portfolio,
):
    """
    Plot the simulated portfolio opportunity set.
    """

    plt.figure(figsize=(10, 6))

    plt.scatter(
        results["volatility"],
        results["return"],
        c=results["sharpe_ratio"],
        cmap="viridis",
        s=10,
        alpha=0.6,
    )

    plt.scatter(
        max_sharpe_portfolio["volatility"],
        max_sharpe_portfolio["return"],
        marker="*",
        s=250,
        label="Maximum Sharpe Ratio",
    )

    plt.scatter(
        min_volatility_portfolio["volatility"],
        min_volatility_portfolio["return"],
        marker="X",
        s=150,
        label="Minimum Volatility",
    )

    plt.xlabel("Annualized Volatility")
    plt.ylabel("Annualized Expected Return")
    plt.title("Monte Carlo Portfolio Opportunity Set")

    plt.colorbar(
        label="Sharpe Ratio"
    )

    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()

    plt.show()


# ============================================================
# Main Execution
# ============================================================

def main():
    """
    Run the complete portfolio analysis.
    """

    print("=" * 60)
    print("PORTFOLIO OPTIMIZATION ANALYSIS")
    print("=" * 60)

    print("\nInvestment universe:")
    print(", ".join(TICKERS))

    print(f"\nData period: {START_DATE} to {END_DATE}")
    print(f"Number of simulated portfolios: {NUM_PORTFOLIOS}")

    # --------------------------------------------------------
    # Download market data
    # --------------------------------------------------------

    prices = download_price_data(
        tickers=TICKERS,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    print("\nDownloaded price data:")
    print(prices.tail())

    # --------------------------------------------------------
    # Calculate historical returns
    # --------------------------------------------------------

    returns = prices.pct_change().dropna()

    print("\nReturn observations:")
    print(f"Number of observations: {len(returns)}")

    # --------------------------------------------------------
    # Run Monte Carlo simulation
    # --------------------------------------------------------

    results = simulate_portfolios(
        returns=returns,
        num_portfolios=NUM_PORTFOLIOS,
        risk_free_rate=RISK_FREE_RATE,
        trading_days=TRADING_DAYS,
        seed=RANDOM_SEED,
    )

    # --------------------------------------------------------
    # Identify key portfolios
    # --------------------------------------------------------

    max_sharpe_portfolio, min_volatility_portfolio = (
        identify_key_portfolios(results)
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print_portfolio_summary(
        portfolio=max_sharpe_portfolio,
        title="Maximum Sharpe Ratio Portfolio",
        tickers=TICKERS,
    )

    print_portfolio_summary(
        portfolio=min_volatility_portfolio,
        title="Minimum Volatility Portfolio",
        tickers=TICKERS,
    )

    # --------------------------------------------------------
    # Save simulation results
    # --------------------------------------------------------

    results.to_csv(
        "portfolio_simulation_results.csv",
        index=False,
    )

    print("\nSimulation results saved to:")
    print("portfolio_simulation_results.csv")

    # --------------------------------------------------------
    # Plot opportunity set
    # --------------------------------------------------------

    plot_portfolio_opportunity_set(
        results=results,
        max_sharpe_portfolio=max_sharpe_portfolio,
        min_volatility_portfolio=min_volatility_portfolio,
    )


if __name__ == "__main__":
    main()
