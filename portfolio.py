"""
Portfolio Analytics Module
Author: Sahand Mostafaei
"""

import numpy as np


def calculate_expected_return(weights, returns):
    """
    Calculate annualized portfolio expected return.
    """

    portfolio_return = np.sum(returns.mean() * weights) * 252

    return portfolio_return



def calculate_volatility(weights, returns):
    """
    Calculate annualized portfolio volatility.
    """

    portfolio_volatility = np.sqrt(
        np.dot(
            weights.T,
            np.dot(
                returns.cov() * 252,
                weights
            )
        )
    )

    return portfolio_volatility



def calculate_sharpe_ratio(weights, returns, risk_free_rate=0.02):
    """
    Calculate annualized Sharpe Ratio.
    """

    portfolio_return = calculate_expected_return(
        weights,
        returns
    )

    portfolio_volatility = calculate_volatility(
        weights,
        returns
    )

    sharpe_ratio = (
        portfolio_return - risk_free_rate
    ) / portfolio_volatility

    return sharpe_ratio
