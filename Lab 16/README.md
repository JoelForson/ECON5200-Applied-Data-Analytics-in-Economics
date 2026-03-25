## High-Dimensional GDP Growth Forecasting with Regularized Regression

**Objective:** Forecast 5-year average GDP per capita growth across 120+ countries using 50+ World Development Indicators, using Ridge and Lasso regularization to address the overfitting inherent in high-dimensional cross-national panels.

---

### Methodology

- **Data acquisition:** Retrieved 35+ WDI indicators spanning trade, macroeconomics, education, infrastructure, health, finance, natural resources, agriculture, and governance (2013–2019) via the `wbgapi` Python API for 120+ countries
- **Feature engineering:** Constructed a country-level cross-section with 5-year average GDP per capita growth as the outcome; applied `StandardScaler` to standardize all predictors prior to regularization
- **Baseline:** Fit an OLS model to establish an overfitting benchmark — confirming that unconstrained estimation collapses under a high p/n ratio
- **Regularization:** Estimated `RidgeCV` and `LassoCV` models with 5-fold cross-validation over a log-spaced λ grid; selected optimal penalty strength via held-out MSE minimization
- **Path analysis:** Traced the full Lasso coefficient path using `lasso_path()` to visualize predictor entry order and identify the λ region balancing sparsity against predictive performance
- **Evaluation:** Compared OLS, Ridge, and Lasso on held-out test R² and MSE to quantify out-of-sample generalization gains from regularization

---

### Key Findings

OLS severely overfitted — training R² was high while test R² was low or negative, consistent with coefficient instability under correlated, high-dimensional predictors. Ridge and Lasso both substantially improved out-of-sample performance by constraining the solution space. Lasso matched Ridge on test R² while retaining a sparse predictor subset, illustrating the bias-variance tradeoff in practice. Critically, zero Lasso coefficients reflect *conditional predictive redundancy* given the WDI correlation structure — not economic irrelevance — a distinction with direct implications for indicator selection in cross-country development research.
