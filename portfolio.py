"""
Portfolio Analytics Module
Author: Sahand Mostafaei
"""

import numpy as np


TRADING_DAYS = 252


def calculate_expected_return(weights, returns):

    return np.sum(returns.mean() * weights) * TRADING_DAYS


def calculate_volatility(weights, returns):

    covariance = returns.cov() * TRADING_DAYS

    return np.sqrt(
        np.dot(
            weights.T,
            np.dot(covariance, weights)
        )
    )


def calculate_sharpe_ratio(
    weights,
    returns,
    risk_free_rate=0.02
):

    portfolio_return = calculate_expected_return(
        weights,
        returns
    )

    portfolio_risk = calculate_volatility(
        weights,
        returns
    )

    return (
        portfolio_return - risk_free_rate
    ) / portfolio_risk


def calculate_sortino_ratio(
    weights,
    returns,
    risk_free_rate=0.02
):

    portfolio_returns = returns.dot(weights)

    downside = portfolio_returns[
        portfolio_returns < 0
    ]

    if len(downside) == 0:
        return np.nan

    downside_deviation = downside.std() * np.sqrt(TRADING_DAYS)

    annual_return = portfolio_returns.mean() * TRADING_DAYS

    return (
        annual_return - risk_free_rate
    ) / downside_deviation
