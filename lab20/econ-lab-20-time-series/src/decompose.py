"""
decompose.py — Reusable time series decomposition utilities.

Covers:
  - Classical decomposition (additive / multiplicative)
  - STL decomposition with optional log-transform
  - MSTL multi-seasonal decomposition
  - Block bootstrap trend confidence intervals
  - ADF + KPSS stationarity suite
  - PELT structural break detection
"""

from __future__ import annotations

import warnings
from typing import Literal

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL, MSTL, seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.stattools import adfuller


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validate_series(series: pd.Series) -> pd.Series:
    """Drop NaNs, ensure DatetimeIndex, return clean copy."""
    s = series.dropna().copy()
    if not isinstance(s.index, pd.DatetimeIndex):
        s.index = pd.DatetimeIndex(s.index)
    if len(s) < 4:
        raise ValueError("Series must have at least 4 observations after dropping NaNs.")
    return s


def detect_frequency(series: pd.Series) -> int:
    """
    Infer the dominant seasonal period from the inferred pandas frequency string.

    Returns
    -------
    int
        12 for monthly, 4 for quarterly, 52 for weekly, 365 for daily, 1 otherwise.
    """
    freq = pd.infer_freq(series.index)
    if freq is None:
        warnings.warn("Could not infer frequency; defaulting to period=12.")
        return 12
    freq = freq.upper()
    mapping = {
        "MS": 12, "M": 12, "ME": 12,
        "QS": 4,  "Q": 4,  "QE": 4,
        "W": 52,
        "D": 365, "B": 261,
        "H": 24,  "T": 60,
    }
    for key, val in mapping.items():
        if freq.startswith(key):
            return val
    warnings.warn(f"Unrecognised frequency '{freq}'; defaulting to period=12.")
    return 12


# ---------------------------------------------------------------------------
# Classical decomposition
# ---------------------------------------------------------------------------

def run_classical(
    series: pd.Series,
    period: int | None = None,
    model: Literal["additive", "multiplicative"] = "additive",
) -> object:
    """
    Classical (moving-average) decomposition.

    Parameters
    ----------
    series : pd.Series
        Raw time series with a DatetimeIndex.
    period : int, optional
        Seasonal period. Auto-detected when None.
    model : {"additive", "multiplicative"}
        Decomposition model. Use "multiplicative" when seasonal amplitude
        scales with the level (e.g. retail sales).

    Returns
    -------
    statsmodels DecomposeResult
    """
    series = _validate_series(series)
    period = period or detect_frequency(series)
    return seasonal_decompose(series, model=model, period=period, extrapolate_trend="freq")


# ---------------------------------------------------------------------------
# STL decomposition
# ---------------------------------------------------------------------------

def run_stl(
    series: pd.Series,
    period: int | None = None,
    robust: bool = True,
    log_transform: bool = False,
) -> object:
    """
    STL (Seasonal-Trend decomposition using LOESS) with optional log-transform.

    Why log_transform?
    ------------------
    STL is an *additive* model: Observed = Trend + Seasonal + Residual.
    When the seasonal amplitude grows proportionally with the trend level
    (multiplicative seasonality), applying STL directly leaks the growing
    seasonal swings into the residual and distorts the seasonal component.
    Taking log(series) converts multiplicative structure to additive:
      log(Observed) = log(Trend) + log(Seasonal) + log(Residual)
    so STL can decompose cleanly and the amplitude stays constant over time.

    Parameters
    ----------
    series : pd.Series
        Raw time series with a DatetimeIndex.
    period : int, optional
        Seasonal period. Auto-detected when None.
    robust : bool
        Use LOESS robustness iterations (downweights outliers).
    log_transform : bool
        Apply log before decomposing; results are in log-space.

    Returns
    -------
    statsmodels STLResults
    """
    series = _validate_series(series)
    period = period or detect_frequency(series)
    if log_transform:
        if (series <= 0).any():
            raise ValueError("log_transform requires all values > 0.")
        series = np.log(series)
    return STL(series, period=period, robust=robust).fit()


# ---------------------------------------------------------------------------
# MSTL — Multi-Seasonal decomposition
# ---------------------------------------------------------------------------

def run_mstl(
    series: pd.Series,
    periods: list[int] | None = None,
    iterate: int = 2,
    stl_kwargs: dict | None = None,
) -> object:
    """
    MSTL (Multiple Seasonal-Trend decomposition using LOESS).

    How MSTL works (iterative seasonal removal)
    --------------------------------------------
    MSTL extends STL to handle series with more than one seasonal cycle
    (e.g. electricity demand with both daily and weekly patterns).
    Algorithm sketch:
      1. Sort periods in ascending order.
      2. Initialise a residual series = original series.
      3. For each seasonal period p_k:
           a. Apply STL to the residual with period=p_k.
           b. Extract the seasonal component S_k.
           c. Subtract S_k from the residual before moving to p_{k+1}.
      4. Apply a final trend extraction (LOESS) to the fully de-seasonalised
         residual.
    Because each pass operates on the residual, the components are
    orthogonal: they don't double-count the same variation. The `iterate`
    parameter controls how many full passes are run — more iterations
    refine the estimates but cost more compute.

    Parameters
    ----------
    series : pd.Series
        Raw time series with a DatetimeIndex.
    periods : list[int], optional
        List of seasonal periods in ascending order (e.g. [24, 168] for
        hourly data with daily + weekly seasonality). Auto-detected (single
        period) when None.
    iterate : int
        Number of full MSTL iterations. 2 is usually sufficient.
    stl_kwargs : dict, optional
        Extra kwargs forwarded to each inner STL call (e.g. {"robust": True}).

    Returns
    -------
    statsmodels MSTLResults
    """
    series = _validate_series(series)
    if periods is None:
        p = detect_frequency(series)
        periods = [p]
    if len(periods) == 0:
        raise ValueError("periods must contain at least one integer.")
    if any(p < 2 for p in periods):
        raise ValueError("All periods must be >= 2.")

    stl_kwargs = stl_kwargs or {}
    return MSTL(series, periods=periods, iterate=iterate, stl_kwargs=stl_kwargs).fit()


# ---------------------------------------------------------------------------
# Block bootstrap trend confidence intervals
# ---------------------------------------------------------------------------

def block_bootstrap_trend(
    series: pd.Series,
    n_bootstrap: int = 500,
    block_size: int | None = None,
    period: int | None = None,
    robust: bool = True,
    alpha: float = 0.05,
    random_state: int | None = 42,
) -> dict:
    """
    Block bootstrap confidence intervals for the STL trend component.

    Why block bootstrap, not i.i.d. bootstrap?
    -------------------------------------------
    Financial and economic time series are serially correlated — today's
    value depends on yesterday's. The standard i.i.d. bootstrap resamples
    *individual* observations at random, which shatters that dependence
    structure and produces residuals that look like white noise even when
    the true residuals are autocorrelated. This leads to confidence
    intervals that are artificially narrow (understated uncertainty).

    Block bootstrap fixes this by resampling *contiguous blocks* of
    consecutive observations. Within each block the autocorrelation is
    preserved exactly (it's the real data in the real order). Only the
    joins between blocks introduce a slight discontinuity — tolerable
    when block_size is chosen appropriately (rule of thumb: ~period or
    sqrt(n) observations).

    Algorithm
    ---------
    1. Fit STL on the original series; extract residuals.
    2. Divide residuals into overlapping blocks of length `block_size`.
    3. Resample blocks with replacement until we have n residuals.
    4. Add each bootstrap residual sequence to the original trend + seasonal.
    5. Re-fit STL on the synthetic series; store the new trend.
    6. Repeat n_bootstrap times; compute quantile-based CIs.

    Parameters
    ----------
    series : pd.Series
        Raw time series with a DatetimeIndex.
    n_bootstrap : int
        Number of bootstrap replications.
    block_size : int, optional
        Length of each resampled block. Defaults to max(period, sqrt(n)).
    period : int, optional
        Seasonal period. Auto-detected when None.
    robust : bool
        Use LOESS robustness iterations in inner STL calls.
    alpha : float
        Significance level for confidence intervals (default 0.05 → 95% CI).
    random_state : int, optional
        Seed for reproducibility.

    Returns
    -------
    dict with keys:
        "trend"        : pd.Series — original STL trend
        "lower"        : pd.Series — (alpha/2) quantile across bootstraps
        "upper"        : pd.Series — (1 - alpha/2) quantile across bootstraps
        "boot_trends"  : np.ndarray — shape (n_bootstrap, n) — all bootstrap trends
    """
    series = _validate_series(series)
    period = period or detect_frequency(series)
    n = len(series)
    block_size = block_size or max(period, int(np.sqrt(n)))

    rng = np.random.default_rng(random_state)

    # --- Step 1: baseline STL ---
    base_result = STL(series, period=period, robust=robust).fit()
    base_trend = base_result.trend.values
    residuals = base_result.resid.values
    seasonal = base_result.seasonal.values

    # --- Steps 2-6: bootstrap ---
    boot_trends = np.empty((n_bootstrap, n))

    for b in range(n_bootstrap):
        # Sample block start indices (with replacement, circular)
        n_blocks = int(np.ceil(n / block_size))
        starts = rng.integers(0, n, size=n_blocks)
        boot_resid = np.concatenate([
            np.take(residuals, np.arange(s, s + block_size) % n)
            for s in starts
        ])[:n]

        # Synthetic series = trend + seasonal + resampled residuals
        synthetic = pd.Series(
            base_trend + seasonal + boot_resid,
            index=series.index,
        )
        try:
            boot_result = STL(synthetic, period=period, robust=robust).fit()
            boot_trends[b] = boot_result.trend.values
        except Exception:
            boot_trends[b] = base_trend  # fallback on rare numerical failure

    lower = pd.Series(np.quantile(boot_trends, alpha / 2, axis=0), index=series.index)
    upper = pd.Series(np.quantile(boot_trends, 1 - alpha / 2, axis=0), index=series.index)

    return {
        "trend": pd.Series(base_trend, index=series.index),
        "lower": lower,
        "upper": upper,
        "boot_trends": boot_trends,
    }


# ---------------------------------------------------------------------------
# Stationarity test suite
# ---------------------------------------------------------------------------

def run_stationarity_suite(
    series: pd.Series,
    regression: Literal["n", "c", "ct", "ctt"] = "ct",
) -> dict:
    """
    Run ADF + KPSS and return a structured result dict with 2×2 verdict.

    ADF null    : unit root present (series is non-stationary)
    KPSS null   : series is stationary

    The regression parameter must match the deterministic structure of the
    series:
      "n"   → no constant, no trend (use only when series fluctuates ~0)
      "c"   → constant only (stationary around a nonzero mean)
      "ct"  → constant + linear trend (most macro series, e.g. GDP)
      "ctt" → constant + quadratic trend (rarely needed)

    Parameters
    ----------
    series : pd.Series
    regression : str
        ADF regression specification (same string passed to KPSS).

    Returns
    -------
    dict with ADF results, KPSS results, and a plain-English verdict.
    """
    series = _validate_series(series)

    # ADF
    adf_stat, adf_p, adf_lags, _, adf_crit, _ = adfuller(series, regression=regression)
    adf_nonstationary = adf_p > 0.05  # fail to reject unit root → non-stationary

    # KPSS — statsmodels uses 'c' / 'ct' (no 'n' or 'ctt')
    kpss_reg = "ct" if "t" in regression else "c"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        kpss_stat, kpss_p, kpss_lags, kpss_crit = kpss(series, regression=kpss_reg, nlags="auto")
    kpss_nonstationary = kpss_p < 0.05  # reject stationarity null → non-stationary

    # 2×2 decision
    if adf_nonstationary and kpss_nonstationary:
        verdict = "Strong unit root — difference the series (I(1))"
        cell = "unit_root"
    elif not adf_nonstationary and kpss_nonstationary:
        verdict = "Trend-stationary — detrend rather than difference"
        cell = "trend_stationary"
    elif adf_nonstationary and not kpss_nonstationary:
        verdict = "Difference-stationary — difference the series"
        cell = "difference_stationary"
    else:
        verdict = "Strongly stationary — model in levels (I(0))"
        cell = "stationary"

    return {
        "adf": {
            "stat": adf_stat, "p": adf_p, "lags": adf_lags,
            "crit": adf_crit, "nonstationary": adf_nonstationary,
        },
        "kpss": {
            "stat": kpss_stat, "p": kpss_p, "lags": kpss_lags,
            "crit": kpss_crit, "nonstationary": kpss_nonstationary,
        },
        "verdict": verdict,
        "cell": cell,
    }


# ---------------------------------------------------------------------------
# PELT structural break detection
# ---------------------------------------------------------------------------

def detect_breaks(
    series: pd.Series,
    penalty: float = 10.0,
    model: str = "rbf",
    min_size: int = 5,
) -> list[pd.Timestamp]:
    """
    Detect structural breaks using the PELT algorithm via ruptures.

    Why does the penalty control the bias-variance tradeoff?
    --------------------------------------------------------
    PELT minimises a cost function of the form:
        C(segmentation) + penalty × (number of breakpoints)
    The cost term rewards fitting the data well (low bias); the penalty
    term penalises complexity — each additional breakpoint costs `penalty`
    units. A small penalty → many breakpoints (overfit / high variance).
    A large penalty → few or no breakpoints (underfit / high bias).
    In practice:
      - BIC-style penalty: penalty = log(n)   → parsimonious, avoids overfitting
      - AIC-style penalty: penalty = 2        → more breakpoints
      - penalty=10 is a reasonable default for macro series; tune visually.

    Parameters
    ----------
    series : pd.Series
    penalty : float
        PELT penalty (higher = fewer breaks detected).
    model : str
        Ruptures cost model: "rbf", "l2", "l1", "normal".
    min_size : int
        Minimum segment length in observations.

    Returns
    -------
    list of pd.Timestamp — dates of detected breakpoints (excluding the end).

    Notes
    -----
    Requires the `ruptures` package. Returns an empty list if ruptures
    is not installed, with a warning.
    """
    series = _validate_series(series)
    try:
        import ruptures as rpt
    except ImportError:
        warnings.warn("ruptures not installed; returning no breakpoints. pip install ruptures")
        return []

    signal = series.values.reshape(-1, 1)
    algo = rpt.Pelt(model=model, min_size=min_size).fit(signal)
    breakpoint_indices = algo.predict(pen=penalty)

    # ruptures returns the index *after* each segment (inclusive of final n)
    dates = [
        series.index[i - 1]
        for i in breakpoint_indices
        if i < len(series)
    ]
    return dates
