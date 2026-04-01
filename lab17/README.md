# NY Fed Yield Curve Recession Model Replication

## Objective
Replicated the Federal Reserve Bank of New York's yield curve recession forecasting model by fitting a logistic regression on FRED macroeconomic data to estimate the probability of an NBER-defined recession occurring within a 12-month horizon.

## Methodology
- Pulled daily T10Y3M (10-Year minus 3-Month Treasury yield spread) and monthly USREC (NBER recession indicator) series directly from FRED via the `fredapi` client, resampling the spread to month-end frequency and applying a 12-month lag to align the predictor with the forecast horizon
- Demonstrated the failure mode of the Linear Probability Model (OLS) on binary outcome data, showing that unconstrained linear regression produces predicted probabilities outside the [0, 1] interval on historical FRED data
- Fit a logistic regression (scikit-learn `LogisticRegression`) to estimate the S-curve relationship between the lagged yield spread and recession probability, with coefficient confidence intervals derived via `statsmodels.Logit`
- Extracted the odds ratio for the yield spread predictor with bootstrapped 90% confidence bands, and evaluated model stability using `TimeSeriesSplit` cross-validation to respect temporal ordering
- Generated the full recession probability time series from 1970 to present, with NBER recession shading and a two-predictor extension comparing the yield spread against a supplementary macro indicator

## Key Findings
The yield spread lagged 12 months is a statistically significant recession predictor (OR ≈ 0.56, p < 0.01), with each 1 percentage point increase in the spread reducing recession odds by approximately 44%. The model correctly elevated recession risk during the 2006–2007 inversion ahead of the Great Recession. During the 2022–2024 inversion — the deepest since the early 1980s — the model assigned peak probabilities near 40–45%, falling short of the 50% decision threshold and ultimately consistent with the absence of an NBER-dated recession, illustrating that probabilistic forecasts communicate risk rather than certainty. A supplementary macro indicator added as a second predictor showed no statistically significant independent contribution (OR ≈ 0.74, p = 0.15), confirming the yield spread as the dominant and most parsimonious signal.
