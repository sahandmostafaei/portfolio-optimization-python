"""
Portfolio Analytics Module

Provides portfolio-level return, risk, Sharpe ratio, and Sortino ratio
calculations for the portfolio optimization analysis.

Author: Sahand Mostafaei
"""

import numpy as np


TRADING_DAYS = 252


def calculate_expected_return(weights, returns):
    """
    Calculate the annualized expected portfolio return.

    Parameters
    ----------
    weights : array-like
        Portfolio weights.
    returns : pandas.DataFrame
        Asset return observations.

    Returns
    -------
    float
        Annualized expected portfolio return.
    """

    weights = np.asarray(weights)

    expected_daily_returns = returns.mean().values

    portfolio_daily_return = np.dot(
        expected_daily_returns,
        weights,
    )

    return portfolio_daily_return * TRADING_DAYS


def calculate_volatility(weights, returns):
    """
    Calculate annualized portfolio volatility.

    Parameters
    ----------
    weights : array-like
        Portfolio weights.
    returns : pandas.DataFrame
        Asset return observations.

    Returns
    -------
    float
        Annualized portfolio volatility.
    """

    weights = np.asarray(weights)

    covariance_matrix = returns.cov().values * TRADING_DAYS

    portfolio_variance = np.dot(
        weights.T,
        np.dot(covariance_matrix, weights),
    )

    return np.sqrt(max(portfolio_variance, 0.0))


def calculate_sharpe_ratio(
    weights,
    returns,
    risk_free_rate=0.02,
):
    """
    Calculate the annualized Sharpe ratio.

    Parameters
    ----------
    weights : array-like
        Portfolio weights.
    returns : pandas.DataFrame
        Asset return observations.
    risk_free_rate : float, default=0.02
        Annualized risk-free rate.

    Returns
    -------
    float
        Annualized Sharpe ratio.
    """

    portfolio_return = calculate_expected_return(
        weights,
        returns,
    )

    portfolio_volatility = calculate_volatility(
        weights,
        returns,
    )

    if portfolio_volatility <= 0:
        return np.nan

    return (
        portfolio_return - risk_free_rate
    ) / portfolio_volatility


def calculate_sortino_ratio(
    weights,
    returns,
    risk_free_rate=0.02,
):
    """
    Calculate the annualized Sortino ratio.

    Downside deviation is calculated from the squared shortfall
    of portfolio returns below a daily minimum acceptable return
    derived from the annual risk-free rate.

    Parameters
    ----------
    weights : array-like
        Portfolio weights.
    returns : pandas.DataFrame
        Asset return observations.
    risk_free_rate : float, default=0.02
        Annualized minimum acceptable return / risk-free rate.

    Returns
    -------
    float
        Annualized Sortino ratio.
    """

    weights = np.asarray(weights)

    portfolio_returns = returns.dot(weights)

    daily_target = (
        (1.0 + risk_free_rate) ** (1.0 / TRADING_DAYS)
        - 1.0
    )

    downside_returns = np.minimum(
        portfolio_returns - daily_target,
        0.0,
    )

    downside_deviation_daily = np.sqrt(
        np.mean(downside_returns ** 2)
    )

    downside_deviation_annualized = (
        downside_deviation_daily
        * np.sqrt(TRADING_DAYS)
    )

    if downside_deviation_annualized <= 0:
        return np.nan

    portfolio_annualized_return = (
        portfolio_returns.mean()
        * TRADING_DAYS
    )

    return (
        portfolio_annualized_return - risk_free_rate
    ) / downside_deviation_annualized
