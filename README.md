# Momentum Trading Project – Final Assignment

This repository contains the code and notebooks for a momentum-based trading strategy project.
The objective is to evaluate whether simple technical momentum signals can improve risk-adjusted
performance relative to buy-and-hold, using a consistent backtesting framework.

## Team Contributions
- **Arin** – Rate-of-Change (ROC) threshold strategy
- **Adrian** – Moving-average crossover strategy
- **Piraveen** – MACD-based momentum strategy
- **Karthikk** – Reusable backtesting framework (`backtest_function.py`)

## Methodology (High-Level)
All strategies:
- Use the same historical price data and backtesting engine
- Generate trading signals based on technical indicators
- Are evaluated using identical performance metrics (returns, number of trades and equity curved)

## Key Findings
- Momentum strategies reduce volatility and drawdowns relative to buy-and-hold
- MACD improves risk-adjusted metrics but sacrifices upside in strong bull markets
- Results are regime-dependent and perform best during market stress periods

## Repository Structure
- `backtest_function.py`  
  Shared backtesting engine (`load_prices`, `run_backtest`, `BacktestResult`) used by all strategies

- `Final_MA_File.ipynb`  
  **Primary notebook for review**  
  Shows the ROC, MA Crossover, MACD strategy end-to-end:
  data loading, indicator construction, signal generation, backtesting,
  plots, with MACD additionally containing QuantStats report, and COVID-period analysis

- Other notebooks (`assignment.ipynb`, `backtesting framework final.ipynb`, etc.)  
  Earlier drafts or exploratory work

## How to Run
Open the final strategy notebook in Jupyter and run all cells from top to bottom.
