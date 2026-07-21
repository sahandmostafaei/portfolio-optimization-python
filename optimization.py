"""
Portfolio Optimization Module
Author: Sahand Mostafaei
"""

import numpy as np

from portfolio import (
    calculate_expected_return,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
)


def generate_random_portfolios(
    returns,
    num_portfolios=5000
):

    num_assets = returns.shape[1]

    results = []

    for _ in range(num_portfolios):

        weights = np.random.random(num_assets)

        weights /= np.sum(weights)

        results.append({

            "weights": weights,

            "return": calculate_expected_return(
                weights,
                returns
            ),

            "risk": calculate_volatility(
                weights,
                returns
            ),

            "sharpe": calculate_sharpe_ratio(
                weights,
                returns
            ),

            "sortino": calculate_sortino_ratio(
                weights,
                returns
            )

        })

    return results


def maximum_sharpe_portfolio(results):

    return max(
        results,
        key=lambda x: x["sharpe"]
    )


def minimum_risk_portfolio(results):

    return min(
        results,
        key=lambda x: x["risk"]
    )
