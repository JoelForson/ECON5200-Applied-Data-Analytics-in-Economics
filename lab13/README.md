# The Architecture of Dimensionality: Hedonic Pricing & the FWL Theorem
### Omitted Variable Bias Forensics — 2026 California Real Estate Metrics

---

## Objective

Architect and manually verify a multivariate hedonic pricing engine against the Frisch-Waugh-Lovell theorem to expose the structural bias introduced by omitted variable contamination and formally prove that OLS achieves ceteris paribus isolation through orthogonal residual decomposition.

---

## Methodology

- **Multivariate OLS Baseline** — Estimated a full hedonic model regressing `Sale_Price` on `Property_Age` and `Distance_to_Tech_Hub` simultaneously using `statsmodels.formula.api`, establishing the ground-truth partial coefficient for property age net of locational effects.

- **Omitted Variable Bias Simulation** — Deliberately misspecified the model by dropping `Distance_to_Tech_Hub` from the regression, isolating the naive univariate age coefficient and quantifying the inflation attributable to the excluded variable's covariance with both the regressor and the outcome.

- **FWL Stage I — Partialling Out the Confounder from the Outcome** — Regressed `Sale_Price` on `Distance_to_Tech_Hub` alone and extracted the residuals, retaining only the variation in price that is orthogonal to — and therefore unexplained by — proximity to the tech hub.

- **FWL Stage II — Partialling Out the Confounder from the Regressor** — Repeated the same procedure with `Property_Age` as the dependent variable, extracting the component of age variation that is statistically independent of distance, thereby purging the shared covariance structure between the two regressors.

- **FWL Stage III — Residuals-on-Residuals Regression** — Regressed the price residuals on the age residuals with no intercept (`-1` specification), mechanically reconstructing the clean partial effect of property age once all dimensional overlap with the confounder had been stripped out.

- **Coefficient Verification** — Confirmed an exact numerical match between the FWL-derived age coefficient and the multivariate OLS estimate, formally validating that the algorithm achieves ceteris paribus through orthogonal projection rather than conceptual approximation.

---

## Key Findings

The naive univariate model — regressing sale price on property age alone — produced a materially inflated depreciation coefficient, incorrectly attributing to the physical age of the home a portion of the value discount that properly belongs to distance from economic infrastructure. This is a textbook manifestation of omitted variable bias: `Distance_to_Tech_Hub` correlates with both older housing stock and lower sale prices, creating a confounded channel that the single-variable model cannot distinguish from genuine structural depreciation.

The FWL proof resolved this contamination with surgical precision. By partialling out the shared variance between distance and both the outcome and the regressor, the theorem reconstructs the exact same coefficient that multivariate OLS produces — not an approximation, but an algebraic identity. This confirms that OLS dimensionality control is not a statistical heuristic but a geometric operation: projecting each variable onto the subspace orthogonal to all included controls and regressing within that purified space. The experiment makes the algorithm's internal mechanics legible — and the cost of misspecification measurable.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Manipulation | pandas |
| Regression Engine | statsmodels.formula.api (Patsy) |
| Visualization | matplotlib |
| Data Source | 2026 California Real Estate Metrics (Zillow Synthetic) |

---

*Part of the Applied Econometrics & Causal Inference portfolio.*
