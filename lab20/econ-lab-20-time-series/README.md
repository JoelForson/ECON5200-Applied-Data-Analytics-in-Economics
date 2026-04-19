# Time Series Diagnostics & Advanced Decomposition

## Objective
This project demonstrates advanced econometric diagnostic techniques for identifying and correcting common specification errors in time series decomposition, stationarity testing, and structural break detection using real-world economic data.

## Methodology
* **STL Decomposition Correction**: Diagnosed multiplicative seasonality misspecification in retail sales data and implemented log-transformation to convert multiplicative structure to additive before applying STL decomposition
* **ADF Test Specification**: Corrected misspecified Augmented Dickey-Fuller tests by implementing appropriate regression parameters (constant + trend) for trended economic series, preventing Type I errors in unit root testing
* **Multi-Seasonal Decomposition**: Applied Multiple STL (MSTL) to simulated hourly electricity demand data, successfully separating overlapping daily (24-hour) and weekly (168-hour) seasonal cycles through iterative seasonal component extraction
* **Bootstrap Uncertainty Quantification**: Implemented moving block bootstrap methodology to generate confidence intervals for GDP trend estimates, preserving autocorrelation structure in residual resampling to avoid overconfident inference
* **Regime-Specific Stationarity Analysis**: Integrated PELT (Pruned Exact Linear Time) structural break detection with per-segment ADF/KPSS testing to evaluate stationarity properties across different economic regimes
* **Production Module Development**: Constructed reusable `decompose.py` module with robust error handling, comprehensive documentation, and standardized interfaces for STL decomposition, stationarity testing, and break detection workflows

## Key Findings
The analysis revealed critical methodological insights for applied time series econometrics:

* **Decomposition Specification Matters**: The original STL implementation on raw retail sales data produced systematically growing seasonal amplitudes (ratio of latest-to-earliest amplitude: 3.2x), violating the additive assumption. Log-transformation correction reduced this ratio to 1.1x, properly isolating seasonal effects.

* **Unit Root Test Sensitivity**: GDP stationarity conclusions were completely reversed when correcting ADF regression specification from 'none' to 'constant + trend' (p-value shifted from <0.01 to >0.10), demonstrating the critical importance of proper deterministic term specification.

* **Structural Break Detection**: GDP growth exhibited significant structural breaks near major economic disruptions (2008 financial crisis, 2020 COVID pandemic), with per-regime stationarity tests showing heterogeneous time series properties across different economic periods.

* **Bootstrap Validation**: Block bootstrap confidence intervals for GDP trend were substantially wider during recession periods (2008, 2020) compared to expansion periods, quantifying the increased uncertainty in trend estimation during economic volatility.

## Technical Implementation
Built using Python ecosystem tools including statsmodels for econometric testing, ruptures for changepoint detection, and FRED API for macroeconomic data access. The production module implements best practices for reproducible economic research with comprehensive error handling and statistical validation.