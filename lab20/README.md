# Time Series Diagnostics & Advanced Decomposition

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![statsmodels](https://img.shields.io/badge/statsmodels-0.14+-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red) ![FRED](https://img.shields.io/badge/data-FRED%20API-orange)

## Overview

A diagnosis-first econometric lab demonstrating how specification errors in time series decomposition, stationarity testing, and structural break detection lead to materially wrong conclusions — and how to fix them. Built around real macroeconomic data from the FRED API.

---

## Objective

Identify and correct six common specification errors in applied time series analysis, implement production-grade tooling in a reusable Python module, and deliver an interactive Streamlit dashboard for parameter sensitivity exploration.

---

## Project Structure

```
econ-lab-20-time-series/
├── README.md
├── requirements.txt
├── notebooks/
│   └── lab_20_time_series.ipynb     ← Step-by-step diagnostic walkthrough
├── src/
│   └── decompose.py                 ← Reusable decomposition module
├── figures/
│   ├── stl_decomposition.png        ← STL before/after log-transform
│   ├── bootstrap_ci.png             ← Block bootstrap trend CI for GDP
│   └── structural_breaks.png        ← PELT break detection output
└── verification-log.md              ← Checkpoint results and parameter validation
```

---

## Methodology

### 1. STL Decomposition Correction
Diagnosed multiplicative seasonality misspecification in retail sales (`RSXFSN`). Applied log-transformation to convert the multiplicative structure (Observed = Trend × Seasonal × Residual) to additive (log(Observed) = log(Trend) + log(Seasonal) + log(Residual)) before running STL. Validated with the seasonal amplitude ratio diagnostic.

### 2. ADF Test Specification
Corrected a misspecified Augmented Dickey-Fuller test that used `regression='n'` (no constant, no trend) on GDP — a series with both a non-zero mean and a deterministic upward trend. Switching to `regression='ct'` reversed the stationarity conclusion entirely, preventing a Type I error that would have incorrectly led to modeling GDP in levels.

### 3. Multi-Seasonal Decomposition (MSTL)
Applied Multiple STL to simulated hourly electricity demand data carrying overlapping daily (period=24) and weekly (period=168) seasonal cycles. MSTL's iterative residual-based extraction isolates each cycle orthogonally, avoiding the double-counting that occurs when single-period STL is applied to multi-seasonal data.

### 4. Block Bootstrap Uncertainty Quantification
Implemented moving block bootstrap for GDP trend confidence intervals. Resampling contiguous blocks preserves the within-block autocorrelation structure that i.i.d. resampling destroys — producing CIs that accurately reflect trend uncertainty rather than understating it.

### 5. Regime-Specific Stationarity Analysis
Integrated PELT (Pruned Exact Linear Time) structural break detection with per-segment ADF/KPSS testing. Evaluated stationarity properties across detected economic regimes, showing that unit root conclusions are not stable across the full sample when structural breaks are present.

### 6. Production Module (`src/decompose.py`)
Constructed a reusable module with type hints, docstrings, and error handling exposing a standardized interface for: classical decomposition, STL (with log-transform option), MSTL, block bootstrap trend CIs, ADF+KPSS stationarity suite with 2×2 decision table, and PELT break detection.

---

## Key Findings

| Finding | Detail |
|---|---|
| Seasonal amplitude ratio (raw STL) | **3.2×** — additive assumption violated |
| Seasonal amplitude ratio (log-transformed STL) | **1.1×** — correctly specified |
| ADF p-value with `regression='n'` | **< 0.01** — falsely rejects unit root |
| ADF p-value with `regression='ct'` | **> 0.10** — correctly fails to reject |
| Structural breaks detected in GDP | 2008 financial crisis, 2020 COVID shock |
| Bootstrap CI width: expansion vs. recession | Materially wider during 2008 and 2020 |

---

## Interactive Dashboard
<img width="961" height="720" alt="Screenshot 2026-04-19 at 1 51 41 AM" src="https://github.com/user-attachments/assets/039e9b9d-6c37-4b39-8171-994266e1f3e2" />

The Streamlit app (`app.py`) lets you explore decomposition sensitivity in real time:

- Enter any FRED series ID
- Toggle between STL / Classical / MSTL
- Enable log-transform and observe the amplitude ratio drop
- Adjust PELT penalty and watch breakpoints appear/disappear
- Enable block bootstrap and vary block size to see CI width change

```bash
cd econ-lab-20-time-series
streamlit run app.py
```

---

## How to Reproduce

### 1. Clone and navigate

```bash
git clone https://github.com/<your-username>/ECON5200-Applied-Data-Analytics-in-Economics.git
cd ECON5200-Applied-Data-Analytics-in-Economics/lab20/econ-lab-20-time-series
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your FRED API key

Get a free key at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html), then:

```bash
export FRED_API_KEY=your_key_here
```

Or paste it directly into the Streamlit sidebar when prompted.

### 4. Run the notebook

```bash
jupyter notebook notebooks/lab_20_time_series.ipynb
```

Execute all cells top-to-bottom. Each step includes a verification checkpoint with expected output ranges.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

**Suggested first run:**
- Series ID: `RSXFSN` (retail sales)
- Method: STL, period=12
- Observe amplitude ratio > 2× → enable log-transform → ratio drops to ~1.1×
- Enable structural breaks at penalty=10 → lower to 3 to see more breaks

### 6. Verify outputs

Check `verification-log.md` for expected checkpoint values. Key thresholds:
- STL amplitude ratio after log-transform: **0.7 – 1.3**
- ADF p-value on GDP with `regression='ct'`: **> 0.05**
- KPSS p-value on GDP with `regression='ct'`: **< 0.05**

---

## Technical Stack

| Library | Purpose |
|---|---|
| `statsmodels` | STL, MSTL, ADF, KPSS |
| `ruptures` | PELT structural break detection |
| `fredapi` | FRED macroeconomic data access |
| `plotly` | Interactive decomposition charts |
| `streamlit` | Dashboard UI |
| `numpy` / `pandas` | Data manipulation |

---

## Concepts Demonstrated

- Additive vs. multiplicative decomposition and the log-transform fix
- ADF regression misspecification and deterministic term selection
- Multi-seasonal time series and iterative seasonal extraction (MSTL)
- Block bootstrap vs. i.i.d. bootstrap for autocorrelated residuals
- PELT penalty as a bias-variance tradeoff in changepoint detection
- ADF + KPSS 2×2 decision table for robust stationarity conclusions

---

*ECON 5200 — Causal Machine Learning & Applied Analytics, Northeastern University*<img width="961" height="720" alt="Screenshot 2026-04-19 at 1 51 41 AM" src="https://github.com/user-attachments/assets/e67af95e-90b3-49b5-a8fb-1e009f843ee3" />
<img width="961" height="731" alt="Screenshot 2026-04-19 at 1 51 00 AM" src="https://github.com/user-attachments/assets/671d9782-35ee-401f-b537-4c3482412e91" />
