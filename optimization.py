"""
Portfolio Optimization Utilities

This module provides reusable functions for:

1. Generating random portfolio weights.
2. Calculating portfolio return.
3. Calculating portfolio volatility.
4. Calculating Sharpe ratio.
5. Calculating Sortino ratio.
6. Calculating a complete set of portfolio performance metrics.

The implementation is intended for Monte Carlo portfolio analysis.
It does not perform formal numerical constrained optimization.
"""

import numpy as np
import pandas as pd


# ============================================================
# Portfolio Weight Generation
# ============================================================

def generate_random_weights(num_assets, rng=None):
    """
    Generate random long-only portfolio weights.

    The weights are drawn from a uniform distribution and then
    normalized so that they sum exactly to 1.

    Parameters
    ----------
    num_assets : int
        Number of assets in the portfolio.

    rng : numpy.random.Generator, optional
        Random number generator. Providing one allows the caller
        to control reproducibility.

    Returns
    -------
    numpy.ndarray
        Portfolio weights that sum to 1.

    Raises
    ------
    ValueError
        If num_assets is less than 1.
    """

    if num_assets < 1:
        raise ValueError(
            "num_assets must be at least 1."
        )

    if rng is None:
        rng = np.random.default_rng()

    weights = rng.random(num_assets)

    weight_sum = weights.sum()

    if weight_sum == 0:
        raise ValueError(
            "Generated portfolio weights sum to zero."
        )

    weights = weights / weight_sum

    return weights


# ============================================================
# Portfolio Return
# ============================================================

def calculate_portfolio_return(
    weights,
    mean_returns,
):
    """
    Calculate annualized expected portfolio return.

    Parameters
    ----------
    weights : numpy.ndarray
        Portfolio asset weights.

    mean_returns : pandas.Series or numpy.ndarray
        Annualized expected asset returns.

    Returns
    -------
    float
        Annualized expected portfolio return.
    """

    weights = np.asarray(weights, dtype=float)
    mean_returns = np.asarray(mean_returns, dtype=float)

    if len(weights) != len(mean_returns):
        raise ValueError(
            "The number of weights must match the number "
            "of asset returns."
        )

    portfolio_return = np.dot(
        weights,
        mean_returns,
    )

    return float(portfolio_return)


# ============================================================
# Portfolio Volatility
# ============================================================

def calculate_portfolio_volatility(
    weights,
    covariance_matrix,
):
    """
    Calculate annualized portfolio volatility.

    Parameters
    ----------
    weights : numpy.ndarray
        Portfolio asset weights.

    covariance_matrix : pandas.DataFrame or numpy.ndarray
        Annualized covariance matrix.

    Returns
    -------
    float
        Annualized portfolio volatility.
    """

    weights = np.asarray(weights, dtype=float)
    covariance_matrix = np.asarray(
        covariance_matrix,
        dtype=float,
    )

    if covariance_matrix.shape != (
        len(weights),
        len(weights),
    ):
        raise ValueError(
            "Covariance matrix dimensions must match "
            "the number of portfolio weights."
        )

    portfolio_variance = np.dot(
        weights,
        np.dot(
            covariance_matrix,
            weights,
        ),
    )

    # Numerical precision can occasionally produce a tiny
    # negative variance such as -1e-16.
    portfolio_variance = max(
        float(portfolio_variance),
        0.0,
    )

    portfolio_volatility = np.sqrt(
        portfolio_variance
    )

    return float(portfolio_volatility)


# ============================================================
# Sharpe Ratio
# ============================================================

def calculate_sharpe_ratio(
    portfolio_return,
    portfolio_volatility,
    risk_free_rate=0.0,
):
    """
    Calculate the annualized Sharpe ratio.

    Parameters
    ----------
    portfolio_return : float
        Annualized portfolio return.

    portfolio_volatility : float
        Annualized portfolio volatility.

    risk_free_rate : float, default=0.0
        Annualized risk-free rate.

    Returns
    -------
    float
        Sharpe ratio.
    """

    if portfolio_volatility <= 0:
        return np.nan

    sharpe_ratio = (
        portfolio_return - risk_free_rate
    ) / portfolio_volatility

    return float(sharpe_ratio)


# ============================================================
# Sortino Ratio
# ============================================================

def calculate_sortino_ratio(
    weights,
    returns,
    risk_free_rate=0.0,
    trading_days=252,
):
    """
    Calculate the annualized Sortino ratio.

    The downside deviation is calculated using daily portfolio
    returns below the daily risk-free threshold.

    Parameters
    ----------
    weights : numpy.ndarray
        Portfolio asset weights.

    returns : pandas.DataFrame
        Historical daily asset returns.

    risk_free_rate : float, default=0.0
        Annualized risk-free rate.

    trading_days : int, default=252
        Number of trading days per year.

    Returns
    -------
    float
        Annualized Sortino ratio.
    """

    if not isinstance(returns, pd.DataFrame):
        returns = pd.DataFrame(returns)

    weights = np.asarray(
        weights,
        dtype=float,
    )

    if returns.shape[1] != len(weights):
        raise ValueError(
            "The number of portfolio weights must match "
            "the number of return series."
        )

    portfolio_daily_returns = returns.dot(weights)

    daily_risk_free_rate = (
        (1 + risk_free_rate) ** (1 / trading_days)
    ) - 1

    daily_excess_returns = (
        portfolio_daily_returns
        - daily_risk_free_rate
    )

    downside_returns = daily_excess_returns[
        daily_excess_returns < 0
    ]

    if downside_returns.empty:
        return np.nan

    downside_deviation = np.sqrt(
        np.mean(
            downside_returns ** 2
        )
    )

    if downside_deviation <= 0:
        return np.nan

    annualized_excess_return = (
        daily_excess_returns.mean()
        * trading_days
    )

    sortino_ratio = (
        annualized_excess_return
        / (
            downside_deviation
            * np.sqrt(trading_days)
        )
    )

    return float(sortino_ratio)


# ============================================================
# Complete Portfolio Metrics
# ============================================================

def calculate_portfolio_metrics(
    weights,
    mean_returns,
    covariance_matrix,
    returns,
    risk_free_rate=0.0,
    trading_days=252,
):
    """
    Calculate the principal performance metrics for a portfolio.

    Parameters
    ----------
    weights : numpy.ndarray
        Portfolio asset weights.

    mean_returns : pandas.Series or numpy.ndarray
        Annualized expected asset returns.

    covariance_matrix : pandas.DataFrame or numpy.ndarray
        Annualized covariance matrix.

    returns : pandas.DataFrame
        Historical daily asset returns.

    risk_free_rate : float, default=0.0
        Annualized risk-free rate.

    trading_days : int, default=252
        Number of trading days per year.

    Returns
    -------
    tuple
        (
            portfolio_return,
            portfolio_volatility,
            sharpe_ratio,
            sortino_ratio
        )
    """

    weights = np.asarray(
        weights,
        dtype=float,
    )

    # --------------------------------------------------------
    # Validate portfolio weights
    # --------------------------------------------------------

    if len(weights) == 0:
        raise ValueError(
            "Portfolio weights cannot be empty."
        )

    if not np.isclose(
        weights.sum(),
        1.0,
        atol=1e-8,
    ):
        raise ValueError(
            "Portfolio weights must sum to 1."
        )

    if np.any(weights < 0):
        raise ValueError(
            "Negative portfolio weights are not allowed."
        )

    # --------------------------------------------------------
    # Calculate portfolio return
    # --------------------------------------------------------

    portfolio_return = calculate_portfolio_return(
        weights=weights,
        mean_returns=mean_returns,
    )

    # --------------------------------------------------------
    # Calculate portfolio volatility
    # --------------------------------------------------------

    portfolio_volatility = calculate_portfolio_volatility(
        weights=weights,
        covariance_matrix=covariance_matrix,
    )

    # --------------------------------------------------------
    # Calculate Sharpe ratio
    # --------------------------------------------------------

    sharpe_ratio = calculate_sharpe_ratio(
        portfolio_return=portfolio_return,
        portfolio_volatility=portfolio_volatility,
        risk_free_rate=risk_free_rate,
    )

    # --------------------------------------------------------
    # Calculate Sortino ratio
    # --------------------------------------------------------

    sortino_ratio = calculate_sortino_ratio(
        weights=weights,
        returns=returns,
        risk_free_rate=risk_free_rate,
        trading_days=trading_days,
    )

    return (
        portfolio_return,
        portfolio_volatility,
        sharpe_ratio,
        sortino_ratio,
    )


# ============================================================
# Convenience Function
# ============================================================

def evaluate_portfolio(
    weights,
    returns,
    risk_free_rate=0.0,
    trading_days=252,
):
    """
    Evaluate a single portfolio directly from historical returns.

    This function is useful when a caller has historical daily
    returns but does not want to manually calculate annualized
    mean returns and covariance matrices.

    Parameters
    ----------
    weights : numpy.ndarray
        Portfolio asset weights.

    returns : pandas.DataFrame
        Historical daily asset returns.

    risk_free_rate : float, default=0.0
        Annualized risk-free rate.

    trading_days : int, default=252
        Number of trading days per year.

    Returns
    -------
    dict
        Portfolio performance metrics.
    """

    if not isinstance(returns, pd.DataFrame):
        returns = pd.DataFrame(returns)

    annualized_mean_returns = (
        returns.mean()
        * trading_days
    )

    annualized_covariance = (
        returns.cov()
        * trading_days
    )

    (
        portfolio_return,
        portfolio_volatility,
        sharpe_ratio,
        sortino_ratio,
    ) = calculate_portfolio_metrics(
        weights=weights,
        mean_returns=annualized_mean_returns,
        covariance_matrix=annualized_covariance,
        returns=returns,
        risk_free_rate=risk_free_rate,
        trading_days=trading_days,
    )

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
    }
