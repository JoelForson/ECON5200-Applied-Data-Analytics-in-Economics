"""
app.py — Interactive Time Series Decomposition Explorer
========================================================
Streamlit app that fetches any FRED series and lets users
explore decomposition methods, stationarity tests, structural
breaks, and block bootstrap trend confidence intervals.

Run:
    streamlit run app.py
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import warnings
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Suppress noisy statsmodels warnings in the UI
warnings.filterwarnings("ignore")

# ── Path setup so we can import our local module ──────────────────────────
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from lab20.src.decompose import (
    run_classical,
    run_stl,
    run_mstl,
    block_bootstrap_trend,
    run_stationarity_suite,
    detect_breaks,
    detect_frequency,
    _validate_series,
)

# ── FRED API ──────────────────────────────────────────────────────────────
try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Time Series Decomposition Explorer",
    page_icon="📈",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────
# Sidebar — Controls
# ─────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔧 Controls")

    st.subheader("Data Source")
    api_key = st.text_input(
        "FRED API Key",
        type="password",
        value=os.getenv("FRED_API_KEY", ""),
        help="Get a free key at https://fred.stlouisfed.org/docs/api/api_key.html",
    )
    series_id = st.text_input(
        "FRED Series ID",
        value="RSXFSN",
        help="Examples: RSXFSN (retail), GDPC1 (GDP), UNRATE (unemployment)",
    )
    start_date = st.date_input("Start date", value=pd.Timestamp("2000-01-01"))

    st.divider()
    st.subheader("Decomposition")
    method = st.selectbox(
        "Method",
        ["STL", "Classical", "MSTL"],
        help="STL: robust LOESS-based | Classical: moving-average | MSTL: multi-seasonal",
    )

    log_transform = st.checkbox(
        "Log-transform (for multiplicative seasonality)",
        value=False,
        help="Converts multiplicative Trend×Seasonal×Residual to additive log-space. "
             "Use when seasonal amplitude grows with the series level.",
    )

    period = st.slider("Primary period", min_value=2, max_value=52, value=12,
                       help="12=monthly, 4=quarterly, 52=weekly")

    if method == "STL":
        robust = st.checkbox("Robust LOESS", value=True,
                             help="Downweights outliers in the LOESS smoother.")

    if method == "MSTL":
        st.markdown("**Secondary period** (for multi-seasonal)")
        period2 = st.slider("Secondary period", 2, 104, 52,
                            help="e.g. 168 for weekly in hourly electricity data")
        robust_mstl = st.checkbox("Robust (MSTL inner STL)", value=True)
        iterate = st.slider("MSTL iterations", 1, 5, 2,
                            help="More iterations refine seasonal estimates; 2 usually sufficient.")

    if method == "Classical":
        cl_model = st.selectbox("Model", ["additive", "multiplicative"])

    st.divider()
    st.subheader("Stationarity Tests")
    adf_reg = st.selectbox(
        "ADF regression",
        ["ct", "c", "n", "ctt"],
        help="ct=constant+trend (GDP) | c=constant only | n=none | ctt=quadratic trend",
    )

    st.divider()
    st.subheader("Structural Breaks (PELT)")
    run_breaks = st.checkbox("Detect structural breaks", value=True)
    penalty = st.slider(
        "PELT penalty",
        min_value=1.0, max_value=100.0, value=10.0, step=1.0,
        help="Higher penalty → fewer breakpoints detected. "
             "Controls the bias-variance tradeoff: low penalty=many breaks (overfit), "
             "high penalty=few breaks (underfit).",
    )

    st.divider()
    st.subheader("Block Bootstrap CI")
    run_boot = st.checkbox("Compute bootstrap trend CI", value=False,
                           help="Computationally intensive — ~30 seconds for n=200 bootstraps.")
    n_bootstrap = st.slider("Bootstrap replications", 50, 500, 200, step=50)
    block_size = st.slider(
        "Block size",
        min_value=2, max_value=52, value=12,
        help="Blocks of consecutive residuals preserve autocorrelation. "
             "Rule of thumb: ~period or sqrt(n) observations.",
    )
    boot_alpha = st.slider("CI level (α)", 0.01, 0.20, 0.05, step=0.01,
                           help="0.05 → 95% confidence interval")

    fetch_btn = st.button("▶ Fetch & Decompose", type="primary", use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────

PLOTLY_COLORS = {
    "observed": "#2c3e50",
    "trend":    "#e67e22",
    "seasonal": "#27ae60",
    "residual": "#c0392b",
    "ci":       "rgba(230, 126, 34, 0.15)",
    "break":    "rgba(155, 89, 182, 0.35)",
}

def make_decomp_figure(
    observed: pd.Series,
    trend: pd.Series,
    seasonal: pd.Series,
    resid: pd.Series,
    title: str,
    breaks: list | None = None,
    boot: dict | None = None,
) -> go.Figure:
    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        subplot_titles=["Observed", "Trend", "Seasonal", "Residual"],
        vertical_spacing=0.06,
    )

    def add_vlines(row):
        if breaks:
            for b in breaks:
                fig.add_vrect(
                    x0=b, x1=b,
                    line=dict(color="purple", dash="dash", width=1.2),
                    row=row, col=1,
                )

    # Row 1 — Observed
    fig.add_trace(go.Scatter(x=observed.index, y=observed.values,
                             line=dict(color=PLOTLY_COLORS["observed"], width=0.9),
                             name="Observed"), row=1, col=1)
    add_vlines(1)

    # Row 2 — Trend (+ bootstrap CI)
    if boot is not None:
        fig.add_trace(go.Scatter(
            x=boot["upper"].index.tolist() + boot["lower"].index.tolist()[::-1],
            y=boot["upper"].values.tolist() + boot["lower"].values.tolist()[::-1],
            fill="toself",
            fillcolor=PLOTLY_COLORS["ci"],
            line=dict(color="rgba(0,0,0,0)"),
            name=f"{int((1-boot_alpha)*100)}% CI",
            showlegend=True,
        ), row=2, col=1)

    fig.add_trace(go.Scatter(x=trend.index, y=trend.values,
                             line=dict(color=PLOTLY_COLORS["trend"], width=1.4),
                             name="Trend"), row=2, col=1)
    add_vlines(2)

    # Row 3 — Seasonal
    fig.add_trace(go.Scatter(x=seasonal.index, y=seasonal.values,
                             line=dict(color=PLOTLY_COLORS["seasonal"], width=0.9),
                             name="Seasonal"), row=3, col=1)
    add_vlines(3)

    # Row 4 — Residual
    fig.add_trace(go.Scatter(x=resid.index, y=resid.values,
                             line=dict(color=PLOTLY_COLORS["residual"], width=0.7),
                             name="Residual"), row=4, col=1)
    fig.add_hline(y=0, line=dict(color="gray", dash="dash", width=0.6), row=4, col=1)
    add_vlines(4)

    fig.update_layout(
        title=dict(text=title, font=dict(size=15)),
        height=700,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=30, t=80, b=40),
        template="plotly_white",
    )
    fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    return fig


def render_stationarity_card(result: dict):
    adf = result["adf"]
    kpss_r = result["kpss"]

    cols = st.columns(2)
    with cols[0]:
        st.markdown("**ADF Test** *(H₀: unit root present)*")
        st.metric("Test statistic", f"{adf['stat']:.4f}")
        st.metric("p-value", f"{adf['p']:.4f}",
                  delta="Non-stationary" if adf["nonstationary"] else "Stationary",
                  delta_color="inverse")
        st.caption(f"Lags: {adf['lags']}")
        for k, v in adf["crit"].items():
            st.caption(f"  {k}: {v:.4f}")

    with cols[1]:
        st.markdown("**KPSS Test** *(H₀: series is stationary)*")
        st.metric("Test statistic", f"{kpss_r['stat']:.4f}")
        st.metric("p-value", f"{kpss_r['p']:.4f}",
                  delta="Non-stationary" if kpss_r["nonstationary"] else "Stationary",
                  delta_color="inverse")
        st.caption(f"Lags: {kpss_r['lags']}")

    verdict_color = {
        "unit_root": "🔴",
        "trend_stationary": "🟡",
        "difference_stationary": "🟡",
        "stationary": "🟢",
    }.get(result["cell"], "⚪")

    st.info(f"{verdict_color} **Verdict:** {result['verdict']}")


def seasonal_amplitude_ratio(seasonal: pd.Series) -> float:
    """Ratio of last year's seasonal range to first year's — should be ~1 for additive."""
    by_year = seasonal.groupby(seasonal.index.year)
    annual_range = by_year.apply(lambda x: x.max() - x.min())
    if len(annual_range) < 2 or annual_range.iloc[0] == 0:
        return float("nan")
    return annual_range.iloc[-1] / annual_range.iloc[0]


# ─────────────────────────────────────────────────────────────────────────
# Main — triggered on button press
# ─────────────────────────────────────────────────────────────────────────
st.title("📈 Time Series Decomposition Explorer")
st.caption(
    "Fetch any FRED series and interactively explore STL / Classical / MSTL decomposition, "
    "stationarity tests, structural breaks, and block bootstrap trend uncertainty."
)

if not fetch_btn:
    st.info(
        "Enter a FRED API key and series ID in the sidebar, then click **▶ Fetch & Decompose**.\n\n"
        "**Quick-start suggestions:**\n"
        "- `RSXFSN` — Retail sales (multiplicative seasonality → try log-transform)\n"
        "- `GDPC1` — Real GDP (unit root, use ADF regression='ct')\n"
        "- `UNRATE` — Unemployment rate\n"
        "- `T10Y2Y` — 10Y-2Y Treasury spread (structural breaks)\n"
    )
    st.stop()

# ── Fetch ─────────────────────────────────────────────────────────────────
if not FRED_AVAILABLE:
    st.error("fredapi is not installed. Run: pip install fredapi")
    st.stop()

if not api_key:
    st.error("Please enter your FRED API key in the sidebar.")
    st.stop()

with st.spinner(f"Fetching {series_id} from FRED…"):
    try:
        fred = Fred(api_key=api_key)
        raw = fred.get_series(series_id, observation_start=str(start_date))
        series = _validate_series(pd.Series(raw))
        auto_period = detect_frequency(series)
    except Exception as e:
        st.error(f"FRED fetch failed: {e}")
        st.stop()

st.success(
    f"Loaded **{series_id}**: {len(series)} observations "
    f"({series.index[0].date()} → {series.index[-1].date()}), "
    f"auto-detected period = {auto_period}"
)

# ── Decompose ─────────────────────────────────────────────────────────────
with st.spinner("Decomposing…"):
    try:
        if method == "STL":
            result = run_stl(series, period=period, robust=robust, log_transform=log_transform)
            obs = result.observed
            trend_s = result.trend
            seasonal_s = result.seasonal
            resid_s = result.resid
            title = f"STL Decomposition — {series_id} (period={period}, robust={robust})"

        elif method == "Classical":
            if log_transform:
                work = np.log(series)
            else:
                work = series
            result = run_classical(work, period=period, model=cl_model)
            obs = result.observed
            trend_s = result.trend
            seasonal_s = result.seasonal
            resid_s = result.resid
            title = f"Classical Decomposition — {series_id} ({cl_model}, period={period})"

        else:  # MSTL
            periods_list = sorted(set([period, period2]))
            result = run_mstl(
                series, periods=periods_list, iterate=iterate,
                stl_kwargs={"robust": robust_mstl},
            )
            obs = pd.Series(result.observed, index=series.index)
            trend_s = pd.Series(result.trend, index=series.index)
            # MSTL returns seasonal as DataFrame; sum all seasonal components
            if hasattr(result.seasonal, "sum"):
                seasonal_s = pd.Series(result.seasonal.sum(axis=1).values, index=series.index)
            else:
                seasonal_s = pd.Series(result.seasonal, index=series.index)
            resid_s = pd.Series(result.resid, index=series.index)
            title = f"MSTL Decomposition — {series_id} (periods={periods_list})"

    except Exception as e:
        st.error(f"Decomposition failed: {e}")
        st.stop()

# ── Structural breaks ─────────────────────────────────────────────────────
breaks = []
if run_breaks:
    with st.spinner("Running PELT break detection…"):
        breaks = detect_breaks(series, penalty=penalty)

# ── Block bootstrap ───────────────────────────────────────────────────────
boot_result = None
if run_boot:
    with st.spinner(f"Block bootstrap ({n_bootstrap} replications)… this may take ~30s"):
        try:
            boot_result = block_bootstrap_trend(
                series,
                n_bootstrap=n_bootstrap,
                block_size=block_size,
                period=period,
                alpha=boot_alpha,
            )
            # Align bootstrap trend CI to our decomposition trend
        except Exception as e:
            st.warning(f"Bootstrap failed: {e}")

# ── Plot ──────────────────────────────────────────────────────────────────
fig = make_decomp_figure(obs, trend_s, seasonal_s, resid_s, title, breaks, boot_result)
st.plotly_chart(fig, use_container_width=True)

# ── Diagnostics ───────────────────────────────────────────────────────────
st.divider()

diag_cols = st.columns([1, 1])

with diag_cols[0]:
    st.subheader("📊 Stationarity Tests")
    with st.spinner("Running ADF + KPSS…"):
        stat_result = run_stationarity_suite(series, regression=adf_reg)
    render_stationarity_card(stat_result)

with diag_cols[1]:
    st.subheader("🔍 Seasonal Amplitude Diagnostic")
    ratio = seasonal_amplitude_ratio(seasonal_s)
    st.metric(
        "Seasonal amplitude ratio (last ÷ first year)",
        f"{ratio:.2f}×",
        help="Should be 0.7–1.3 for a correctly specified additive model. "
             ">> 1 suggests multiplicative seasonality leaking into components.",
    )
    if not np.isnan(ratio):
        if 0.7 <= ratio <= 1.3:
            st.success("✅ Amplitude roughly constant — additive model is well-specified.")
        elif ratio > 2.0:
            st.error(
                "❌ Amplitude growing strongly. Consider enabling **log-transform** "
                "to correct the multiplicative seasonality violation."
            )
        else:
            st.warning("⚠️ Mild amplitude growth. Log-transform may improve fit.")

    st.markdown("**Seasonal amplitude by year (last 10)**")
    by_year = seasonal_s.groupby(seasonal_s.index.year)
    amp_df = by_year.apply(lambda x: x.max() - x.min()).tail(10).rename("amplitude")
    st.bar_chart(amp_df)

# ── Structural breaks summary ─────────────────────────────────────────────
if run_breaks:
    st.divider()
    st.subheader("🔴 Structural Breaks (PELT)")
    if breaks:
        st.markdown(
            f"Detected **{len(breaks)} break(s)** with penalty={penalty}. "
            "Breaks appear as dashed purple lines in the decomposition plot above."
        )
        st.dataframe(pd.DataFrame({"Break date": breaks}), use_container_width=True)
    else:
        st.info(f"No structural breaks detected at penalty={penalty}. "
                "Try lowering the penalty to detect smaller shifts.")

    st.caption(
        "**PELT penalty tradeoff:** Low penalty → many breakpoints (overfits noise). "
        "High penalty → fewer breakpoints (may miss real structural shifts). "
        "Use BIC-style heuristic: penalty ≈ log(n) as a starting point."
    )

# ── Bootstrap CI summary ──────────────────────────────────────────────────
if boot_result is not None:
    st.divider()
    st.subheader("🎲 Block Bootstrap Trend CI")
    ci_width = (boot_result["upper"] - boot_result["lower"]).mean()
    st.metric("Mean CI width", f"{ci_width:.4f}")
    st.caption(
        f"Block size = {block_size} observations. "
        "Block bootstrap preserves within-block autocorrelation; "
        "i.i.d. bootstrap would destroy it, producing artificially narrow intervals."
    )

# ── Sensitivity explainer ─────────────────────────────────────────────────
st.divider()
with st.expander("📖 What does this app reveal about decomposition sensitivity?"):
    st.markdown("""
**What parameter choices expose:**

1. **Period selection** is the most consequential choice. A wrong period
   (e.g. 4 instead of 12 for monthly data) causes the seasonal component
   to mis-align, pushing aliased variation into the residual. The seasonal
   amplitude diagnostic immediately flags this.

2. **Log-transform vs. raw**: for series with multiplicative seasonality
   (retail sales, industrial production), the amplitude ratio diagnostic
   will show a ratio >> 1 on the raw series. After enabling log-transform
   it should drop to 0.7–1.3. This is the single most common
   misspecification in practice.

3. **STL robust vs. non-robust**: when outliers are present (COVID-era
   data, financial crises), non-robust STL absorbs shocks into the trend,
   making structural breaks appear "smooth." Robust STL isolates them in
   the residual, giving the break detector a cleaner signal.

4. **PELT penalty**: dragging the slider from 1 to 100 shows how the
   number of detected breaks monotonically decreases. The optimal penalty
   is usually around log(n) — above that, real structural shifts start
   getting absorbed into a single segment.

5. **Bootstrap block size**: a block size of 1 is equivalent to i.i.d.
   resampling (destroys autocorrelation → intervals too narrow). As
   block size increases toward the series length, the CI widens to
   reflect genuine trend uncertainty. The "right" block size is
   typically the dominant autocorrelation lag or the seasonal period.

**Bottom line:** Decomposition is not a black box — every parameter
choice embeds an assumption about the data-generating process. This
app makes those assumptions visible and testable.
    """)
