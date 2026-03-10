# Architecting the Prediction Engine
### Multivariate OLS Real Estate Valuation — Zillow ZHVI 2026 Micro Dataset

---

## Objective

Engineer a production-grade multivariate OLS prediction engine trained on cross-sectional real estate market data to forecast residential valuations, calibrate algorithmic business risk, and validate out-of-sample performance via loss minimization.

---

## Methodology

- **Data Sourcing & Preparation** — Ingested the Zillow Home Value Index (ZHVI) 2026 Micro Dataset, a cross-sectional snapshot of contemporary U.S. residential market conditions, and executed structured preprocessing using `pandas` to enforce type integrity and eliminate estimation-contaminating records.

- **Feature Engineering via Patsy Formula API** — Leveraged `statsmodels`' Patsy formula interface to declaratively specify the design matrix, enabling rapid iteration over hedonic attribute combinations without manual array construction.

- **OLS Model Estimation** — Fitted a multivariate Ordinary Least Squares regression using `statsmodels.formula.api`, extracting the full coefficient vector, standard errors, t-statistics, and p-values to assess the marginal contribution of each property attribute to market valuation.

- **Paradigm Shift — Explanation to Prediction** — Deliberately reoriented the analytical objective from classical inferential explanation (interpreting β coefficients) to predictive engineering: generating out-of-sample fitted values and evaluating the model on forecast accuracy rather than statistical significance alone.

- **Loss Quantification via Dollar-Denominated RMSE** — Computed the Root Mean Squared Error (RMSE) on the original price scale in U.S. Dollars — not log-transformed units — to translate abstract statistical loss into a concrete, business-interpretable financial error margin directly comparable to real-world valuation tolerances.

---

## Key Findings

The OLS engine successfully converged on a stable parameter solution across the ZHVI feature space, with the hedonic attribute set explaining a substantial share of cross-sectional variance in residential valuations. The critical analytical output was not the coefficient table, but the **dollar-denominated RMSE** — a precision metric that reframes model evaluation from an academic exercise into an operational risk assessment. By grounding prediction error in actual USD, the model's performance ceiling and failure modes become directly legible to non-technical stakeholders: underwriters, portfolio managers, and acquisition analysts who require error bounds in financial — not statistical — terms. This exercise established a replicable framework for treating OLS not merely as an explanatory tool, but as a deployable forecasting engine with a quantifiable and auditable error budget.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Data Manipulation | pandas, numpy |
| Regression Engine | statsmodels (Patsy Formula API) |
| Data Source | Zillow ZHVI 2026 Micro Dataset |

---

*Part of the Applied Econometrics & Predictive Modeling portfolio.*
