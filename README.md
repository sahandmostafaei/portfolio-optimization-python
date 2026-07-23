# Portfolio Optimization & Asset Allocation

## Overview

This project implements Modern Portfolio Theory (MPT) to construct and evaluate investment portfolios using historical market data.

The application retrieves financial market data directly from Yahoo Finance, calculates portfolio statistics, generates thousands of random portfolios using Monte Carlo simulation, and identifies optimal portfolios based on risk-adjusted performance.

The project demonstrates quantitative finance concepts commonly used in portfolio management, investment analysis, and asset allocation.

---

## Objectives

- Download historical market data automatically
- Calculate daily and annualized returns
- Compute portfolio volatility
- Perform Monte Carlo portfolio simulation
- Maximize the Sharpe Ratio
- Identify the Minimum Risk Portfolio
- Calculate the Sortino Ratio
- Generate the Efficient Frontier
- Analyse correlation and covariance between assets

---

## Data Source

Historical market data is retrieved directly from **Yahoo Finance** using the **yfinance** Python package.

The project automatically downloads market prices when executed, ensuring that portfolio optimization is performed using up-to-date financial data.

The `data/` directory is reserved for optional cached datasets and therefore does not contain stock price CSV files by default.

---

## Features

- Automatic retrieval of historical market data using Yahoo Finance (`yfinance`)
- Portfolio return calculation
- Portfolio volatility calculation
- Monte Carlo simulation
- Modern Portfolio Theory implementation
- Efficient Frontier visualization
- Maximum Sharpe Ratio portfolio
- Minimum Risk portfolio
- Sortino Ratio calculation
- Correlation matrix
- Covariance matrix
- Portfolio allocation reporting

---

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- yfinance

---

## Repository Structure

```text
portfolio-optimization-python/

├── data/
│   └── README.md

├── figures/

├── portfolio.py
├── optimization.py
├── statistics.py
├── visualization.py
├── main.py

├── PROJECT.md
├── RESULTS.md
├── ROADMAP.md
├── CHANGELOG.md

├── README.md
├── requirements.txt
├── LICENSE
```

---

## Workflow

1. Download historical market prices from Yahoo Finance
2. Calculate daily returns
3. Compute correlation and covariance matrices
4. Generate random portfolios
5. Calculate expected return and portfolio risk
6. Compute Sharpe Ratio and Sortino Ratio
7. Identify optimal portfolios
8. Plot the Efficient Frontier
9. Display portfolio allocation results

---

## Financial Concepts

- Modern Portfolio Theory
- Asset Allocation
- Portfolio Optimization
- Diversification
- Expected Return
- Portfolio Volatility
- Sharpe Ratio
- Sortino Ratio
- Efficient Frontier
- Risk Management

---

## Applications

This project demonstrates analytical techniques used in:

- Investment Management
- Wealth Management
- Portfolio Construction
- Quantitative Finance
- Asset Management
- Financial Analytics

---

## Future Improvements

- CAPM expected returns
- Black-Litterman portfolio optimization
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)
- Interactive dashboard
- Additional optimization methods

---

## Author

**Sahand Mostafaei**

Bachelor of Science in Electrical Engineering

Interested in Banking, Investment Management, Quantitative Finance, Financial Risk Management, and Data Analytics.

---

## Disclaimer

This project is intended for educational purposes only and should not be considered investment or financial advice.
