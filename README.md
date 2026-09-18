# Portfolio Optimization in Python

A quantitative portfolio-analysis project examining the relationship between portfolio expected return, volatility, and risk-adjusted performance using historical financial-market data.

The project uses Monte Carlo simulation to generate feasible portfolios and analyze their risk–return characteristics.

## Overview

Portfolio construction involves balancing expected return against investment risk while considering diversification and investor constraints.

This project develops a Python-based framework for:

- Historical market-data retrieval
- Return calculation
- Portfolio return estimation
- Portfolio volatility estimation
- Sharpe ratio analysis
- Sortino ratio analysis
- Monte Carlo portfolio simulation
- Portfolio risk–return visualization
- Asset-level and portfolio-level analysis

The project is intended as a quantitative finance demonstration of portfolio theory implemented in Python.

## Investment Universe

The analysis uses a diversified set of exchange-traded assets representing different asset classes and market exposures.

The portfolio universe includes:

- SPY — U.S. equities
- EFA — Developed-market equities outside the U.S.
- EEM — Emerging-market equities
- TLT — U.S. long-duration Treasury bonds
- GLD — Gold
- DBC — Broad commodities
- VNQ — U.S. real estate investment trusts

The combination provides exposure to equities, fixed income, commodities, and real estate.

## Methodology

The project follows a standard quantitative portfolio-analysis workflow.

Historical price data
      ↓
Adjusted-price data
      ↓
Return calculation
      ↓
Portfolio simulation
      ↓
Expected return and volatility
      ↓
Sharpe and Sortino ratios
      ↓
Risk–return analysis
      ↓
Portfolio visualization

## Data

Historical market data are retrieved using the `yfinance` Python package.

The analysis uses adjusted market prices where available so that the return calculations are designed to account for distributions and other relevant price adjustments reflected in the adjusted series.

Returns are calculated from the historical observations and used as the basis for portfolio-level calculations.

## Portfolio Construction

The Monte Carlo component generates random portfolio-weight combinations subject to the portfolio constraints implemented in the project.

For each simulated portfolio, the framework calculates:

- Expected annualized return
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Portfolio weights

The simulated portfolios are then used to examine the feasible risk–return opportunity set.

## Monte Carlo Portfolio Opportunity Set

The project visualizes simulated portfolios in expected-return and volatility space.

This produces a Monte Carlo portfolio opportunity set showing the distribution of feasible portfolios under the specified constraints.

The simulated opportunity set should be distinguished from a formally optimized mathematical efficient frontier.

A formal efficient frontier requires solving an optimization problem for a sequence of target-return or risk constraints. The present project focuses on Monte Carlo simulation and portfolio analytics rather than claiming that the simulated scatter itself is the exact efficient frontier.

## Portfolio Return

Portfolio expected return is calculated from the weighted expected returns of the underlying assets.

The annualized expected return is:

Portfolio Return = Σ(wᵢ × E[Rᵢ]) × 252

where:

- wᵢ is the portfolio weight of asset i
- E[Rᵢ] is the mean daily return of asset i
- 252 represents the approximate number of trading days per year

## Portfolio Risk

Portfolio volatility is calculated using the covariance matrix of asset returns.

The portfolio variance is:

σₚ² = wᵀΣw

where:

- w is the vector of portfolio weights
- Σ is the covariance matrix of asset returns

Volatility is then annualized using the square root of the approximate number of trading days.

## Sharpe Ratio

The Sharpe ratio measures excess portfolio return relative to portfolio volatility.

Sharpe Ratio = (Rₚ − Rf) / σₚ

where:

- Rₚ is annualized portfolio return
- Rf is the annualized risk-free rate
- σₚ is annualized portfolio volatility

The default risk-free rate used by the analytical functions is 2%, unless another value is supplied.

## Sortino Ratio

The Sortino ratio evaluates portfolio performance relative to downside risk rather than total volatility.

Sortino Ratio = (Rₚ − MAR) / Downside Deviation

where:

- Rₚ is annualized portfolio return
- MAR is the minimum acceptable return
- Downside Deviation measures the dispersion of returns below the target

The implementation calculates downside deviation from the squared shortfall of portfolio returns below a daily target derived from the annual risk-free rate.

## Risk–Return Analysis

The project examines the trade-off between expected return and portfolio risk across the simulated portfolios.

The resulting analysis can be used to investigate:

- Diversification effects
- Portfolio volatility
- Expected-return dispersion
- Risk-adjusted performance
- The relationship between portfolio composition and risk
- The effect of combining assets with different return characteristics

## Visualizations

The project generates visualizations of the simulated portfolio universe and related portfolio statistics.

Typical outputs include:

- Simulated portfolio risk–return distributions
- Portfolio performance comparisons
- Asset-level return characteristics
- Portfolio risk metrics

Generated figures are stored in the `figures/` directory.

## Project Structure

portfolio-optimization-python/
│
├── data/
│   └── market data
│
├── figures/
│   └── generated figures
│
├── optimization.py
├── portfolio.py
├── visualization.py
├── main.py
├── requirements.txt
├── PROJECT.md
└── README.md

## Source Modules

| Module | Purpose |
|---|---|
| `optimization.py` | Portfolio simulation and optimization-related calculations |
| `portfolio.py` | Portfolio return, volatility, Sharpe ratio, and Sortino ratio calculations |
| `visualization.py` | Portfolio and risk–return visualizations |
| `main.py` | Main analytical workflow |

## Key Quantitative Finance Concepts

The project demonstrates practical implementation of:

- Modern Portfolio Theory
- Diversification
- Portfolio expected return
- Covariance matrices
- Portfolio volatility
- Risk-adjusted performance
- Sharpe ratio
- Sortino ratio
- Monte Carlo simulation
- Asset allocation
- Risk–return analysis

## Technical Skills

- Python
- pandas
- NumPy
- SciPy
- Matplotlib
- yfinance
- Quantitative finance
- Financial data analysis
- Portfolio analytics
- Statistical analysis

## Limitations

The Monte Carlo approach provides a simulated opportunity set rather than an analytically derived efficient frontier.

The analysis also relies on historical return characteristics, which may not persist in future market conditions.

Additional extensions could include:

- Formal mean-variance optimization
- Long-only optimization constraints
- Target-return optimization
- Maximum-Sharpe optimization
- Minimum-variance optimization
- Alternative risk measures
- Robust covariance estimation
- Transaction costs
- Portfolio turnover constraints
- Out-of-sample evaluation

## Interpretation

The project is designed to demonstrate the implementation of portfolio theory and quantitative investment analysis rather than to provide investment recommendations.

Historical simulations and portfolio statistics should therefore be interpreted as analytical outputs rather than forecasts of future investment performance.

## Disclaimer

This project is intended for educational, research, and portfolio purposes.

The analysis does not constitute investment advice or a recommendation to buy or sell any security.
