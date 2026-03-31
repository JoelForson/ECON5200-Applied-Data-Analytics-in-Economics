## AI Capex Diagnostic Modeling

**Objective:** Diagnosed structural violations in an OLS regression model predicting AI software revenue from Nvidia's 2026 capital expenditure and deployment data, applying heteroscedasticity-robust estimation to recover valid statistical inference.

**Methodology:**
- Specified a baseline OLS model using `statsmodels` with AI deployment metrics as predictors of software revenue, establishing a naive benchmark for comparison
- Conducted residual diagnostics via scatter plots and scale-location plots (matplotlib/seaborn) to visually identify heteroscedasticity patterns across capital expenditure tiers
- Computed Variance Inflation Factors (VIF) for all predictors to assess multicollinearity and its potential distortion of coefficient stability
- Applied HC3 heteroscedasticity-consistent standard errors (MacKinnon-White estimator) to correct false precision in the naive model's inference, without altering point estimates
- Compared naive and robust model outputs side-by-side to quantify the degree to which uncorrected SEs understated true sampling uncertainty

**Key Findings:** The naive OLS model exhibited severe heteroscedasticity concentrated at high capital expenditure tiers, where error variance expanded systematically with fitted values — a pattern consistent with scale effects in large-cap AI infrastructure investment. This structural violation artificially compressed standard errors, producing misleadingly low p-values that overstated the statistical significance of deployment metrics. Correcting with HC3 robust estimators appropriately widened standard errors, revealing that several coefficients previously significant at conventional thresholds no longer met that bar — a finding with direct implications for how deployment data should be interpreted in AI revenue forecasting contexts.

**Tech Stack:** Python · pandas · statsmodels · matplotlib · seaborn
