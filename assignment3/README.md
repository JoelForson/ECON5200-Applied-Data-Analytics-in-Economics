# Econ_5200 Assignment 3 — The Causal Architecture
**SwiftCart Logistics | Senior Data Economist**

A computational econometrics project that replaces fragile parametric assumptions with heavy computation to build empirical evidence and isolate pure causality from spurious correlation across three business-critical problems.

---

## Project Structure

```
Econ_5200_Assignment_3_Causal/
│
├── Econ_5200_Assignment_3_Causal.ipynb   # Main notebook (Google Colab)
├── swiftcart_loyalty.csv                  # Loyalty program observational dataset
├── love_plot_swiftcart.png                # PSM covariate balance visualization
└── README.md
```

---

## The Mission

The SwiftCart executive board is paralyzed by contradictory data on three fronts. This project cuts through the statistical noise:

| Problem | Method | Claim Under Investigation |
|---|---|---|
| Driver tip compensation equity | Bootstrap CI | "Median driver compensation is fair" |
| Batch routing algorithm efficacy | Permutation Test | "New routing reduces delivery times" |
| SwiftPass loyalty ROI | Propensity Score Matching | "Subscribers spend 300% more" |

---

## Phase 1 — Bootstrapping Non-Parametric Uncertainty

**Context:** Tip data is zero-inflated (100 of 250 drivers tip exactly $0) and right-skewed by outliers. The Central Limit Theorem fails here — parametric confidence intervals are invalid.

**Method:** Manual bootstrap engine. 10,000 resamples with replacement → compute median each iteration → extract 2.5th and 97.5th percentiles for the 95% CI.

```python
for i in range(10_000):
    resample = driver_tips[np.random.randint(0, n, size=n)]
    bootstrap_medians[i] = np.median(resample)

ci_lower = np.percentile(bootstrap_medians, 2.5)
ci_upper = np.percentile(bootstrap_medians, 97.5)
```

**Key Output:** The CI is asymmetric — the upper margin exceeds the lower margin. This asymmetry is direct evidence of the right skew in the underlying distribution and proves parametric symmetric CIs would have been misleading.

> ⚠️ `scipy.stats.bootstrap` is intentionally not used. All iterative machinery is written manually per the "Foundations First" academic protocol.

---

## Phase 2 — Exact Non-Parametric Permutation Testing

**Context:** The A/B test (500 Control, 500 Treatment) has extreme upper-bound outliers in the treatment group caused by software crash loops. Homoscedasticity is violated — a standard T-test is invalid.

**Data generating process:**
- Control: `Normal(mean=35, sd=5)`
- Treatment: `LogNormal(mean=3.4, sigma=0.4)` — fast on average, catastrophic at the tail

**Method:** Permutation test with 5,000 iterations. Under the null hypothesis, group labels are arbitrary. Shuffle the full combined array, split into two pseudo-groups of 500, record the difference in means. The empirical p-value = proportion of permutations at least as extreme as the observed difference.

```python
for i in range(5_000):
    shuffled = np.random.permutation(combined)
    permuted_diffs[i] = shuffled[:500].mean() - shuffled[500:].mean()

p_value = np.mean(np.abs(permuted_diffs) >= np.abs(observed_diff))
```

**Key Output:** A two-tailed empirical p-value that makes zero distributional assumptions — valid even under heavy right skew and heteroscedasticity.

> ⚠️ `scipy.stats.permutation_test` is intentionally not used per the "Foundations First" protocol.

---

## Phase 3 — Propensity Score Matching (Causal Inference)

**Context:** Marketing claims SwiftPass subscribers spend 300% more. This is almost certainly selection bias — power users self-select into the program because cumulative fee savings are worth it to them. They were already high spenders before the program existed.

**Dataset:** `swiftcart_loyalty.csv` — 8,941 users with pre-treatment covariates and post-treatment spending.

| Column | Description |
|---|---|
| `subscriber` | Treatment indicator (D=1 subscriber, D=0 control) |
| `pre_spend` | Pre-treatment monthly order volume ($) |
| `account_age` | Account age in months |
| `support_tickets` | Historical support ticket count |
| `post_spend` | Post-treatment monthly spending ($) — outcome |

**Pipeline:**

1. **Naive SDO** — raw difference in means between subscribers and non-subscribers (confounded)
2. **Propensity Score Estimation** — `LogisticRegression` on pre-treatment covariates predicts P(subscribe)
3. **1:1 Nearest-Neighbor Matching** — `NearestNeighbors` links each subscriber to the closest non-subscriber by propensity score
4. **ATT** — Average Treatment Effect on the Treated computed from matched pairs only

```python
logit = LogisticRegression(max_iter=1000)
logit.fit(X_scaled, D)
df['propensity_score'] = logit.predict_proba(X_scaled)[:, 1]

nn = NearestNeighbors(n_neighbors=1)
nn.fit(control[['propensity_score']])
distances, indices = nn.kneighbors(treated[['propensity_score']])
```

**Bias decomposition:**
```
Selection Bias Component = Naive SDO − Causal ATT
```

The gap between these two numbers is the dollar-denominated cost of the marketing team's flawed analysis.

---

## Phase 4 — Love Plot: Covariate Balance Visualization

A Love Plot (Standardized Mean Differences) visually confirms that PSM successfully mitigated selection bias across all pre-treatment covariates.

**SMD formula (Austin 2011):**
```
SMD = (mean_treated − mean_control) / pooled_std
```

**Balance threshold:** |SMD| < 0.10 (10% rule)

**Reading the plot:**
- 🔴 Red circles = Before matching (raw bias — dots far from zero prove selection bias existed)
- 🔷 Teal diamonds = After matching (residual bias — must fall inside the ±0.10 band)
- Connector lines pointing inward = matching improved balance on every covariate

![Love Plot](love_plot_swiftcart.png)

---

## Setup

```python
# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
```

No additional dependencies beyond a standard Colab/Anaconda environment.

---

## Key Findings Summary

| Analysis | Naive Estimate | Causal Estimate | Bias Detected |
|---|---|---|---|
| Driver Tip Median CI | Symmetric (parametric) | Asymmetric (bootstrap) | ✅ CLT violation |
| Routing Algorithm p-value | T-test (invalid) | Permutation (exact) | ✅ Heteroscedasticity |
| SwiftPass Spend Lift | ~300% (SDO) | Materially lower (ATT) | ✅ Selection bias |

---

## Academic Protocol

> **Strict Prohibition — Phases 1 & 2:** `scipy.stats.bootstrap` and `scipy.stats.permutation_test` are forbidden. All iterative engines are written manually using native NumPy vectorization to demonstrate comprehension of the underlying mathematical machinery.

> **LLM Authorization:** Generative AI authorized exclusively for Phase 4 visualization expansion.

---

*ECON 5200 Applied Data Analytics | Northeastern University*
