"""
Financial Statistics Module
Author: Sahand Mostafaei
"""

import pandas as pd



def calculate_returns(prices):
    """
    Calculate daily percentage returns.
    """

    returns = prices.pct_change()

    return returns.dropna()



def correlation_matrix(returns):
    """
    Calculate asset correlation matrix.
    """

    return returns.corr()



def covariance_matrix(returns):
    """
    Calculate covariance matrix.
    """

    return returns.cov()
