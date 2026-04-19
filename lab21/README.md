Based on your actual results from the lab (alpha+beta = 0.9826, half-life = 39.5 days), here's your README:

---

# Time Series Forecasting — ARIMA, GARCH & Bootstrap

**Objective:** Diagnose and correct a misspecified ARIMA pipeline on U.S. CPI data, extend the analysis to model S&P 500 conditional volatility using GARCH(1,1), and implement distribution-free forecast uncertainty quantification via block bootstrap resampling.

## Methodology

- Identified three deliberate errors in a broken ARIMA pipeline: fitting on non-stationary levels (d=0), omitting monthly seasonality structure, and skipping Ljung-Box residual diagnostics before forecasting
- Verified first-difference stationarity of CPI using ADF and KPSS tests, confirming I(1) behavior consistent with the macroeconomics literature
- Corrected the pipeline to SARIMA using `pmdarima.auto_arima` with `d=1`, `m=12`, and a full grid search over seasonal AR/MA orders; validated clean residuals via Ljung-Box at lags 12 and 24
- Fit GARCH(1,1) to 6,287 daily S&P 500 log returns (2000–2024), modeling conditional variance as a function of lagged squared residuals and lagged variance
- Implemented a moving block bootstrap to generate distribution-free 95% forecast intervals for the SARIMA model, preserving residual autocorrelation and heteroskedasticity structure
- Built a reusable `forecast_evaluation.py` module implementing `compute_mase()` and `backtest_expanding_window()` for production-grade expanding-window forecast evaluation

## Key Findings

- S&P 500 volatility exhibits high persistence: α + β = 0.9826, implying a volatility shock half-life of approximately 39.5 trading days — consistent with well-documented long-memory behavior in equity markets
- Block bootstrap confidence intervals were wider than standard parametric ARIMA intervals, reflecting the fat-tailed, heteroskedastic nature of CPI forecast errors that normality assumptions would understate
- SARIMA with `D=0` outperformed models with seasonal differencing on this series, suggesting CPI seasonality is better captured through seasonal AR/MA terms than by differencing — an empirically important distinction for inflation forecasting
