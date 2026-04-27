import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MW DiD Dashboard", layout="wide")

# ── PASTE YOUR FITTED VALUES HERE ──────────────────────────────────────────
# Run these lines in your notebook and copy the output:
#   print(res_twfe.params['log_mw_real'])
#   print(res_twfe.std_errors['log_mw_real'])
#   print(naive_est)

CAUSAL_EST = -0.4477997000532203   # e.g. 0.412
CAUSAL_SE  = 0.4343204332288955    # e.g. 0.183
NAIVE_EST  = 1.9790919700030642    # e.g. -0.091
# ───────────────────────────────────────────────────────────────────────────

st.title("Minimum Wage & Unemployment: Causal Effect Dashboard")
st.markdown(
    "**Causal question:** Does raising the state minimum wage increase unemployment?  \n"
    "**Method:** Two-Way Fixed Effects DiD (state + quarter FE, SEs clustered by state)  \n"
    "**Data:** FRED LAUS + DOL minimum wage, 50 states, 2000–2022"
)

if CAUSAL_EST == 0.0:
    st.warning(
        "⚠️  Placeholder estimates detected. "
        "Open `app.py` and paste your fitted values into CAUSAL_EST, CAUSAL_SE, and NAIVE_EST."
    )

# ── SIDEBAR ────────────────────────────────────────────────────────────────
st.sidebar.header("What-if scenario")
mw_change_pct = st.sidebar.slider(
    "Minimum wage increase (%)", min_value=1, max_value=50, value=10, step=1
)
st.sidebar.markdown(
    "Move the slider to see how different sizes of minimum wage hikes "
    "translate into estimated unemployment effects under the causal model."
)

# ── POINT ESTIMATE FOR SELECTED SLIDER VALUE ────────────────────────────────
# β is the effect of a 1-unit increase in log(real MW)
# A p% increase → log(1 + p/100) change in log MW
log_change = np.log(1 + mw_change_pct / 100)
effect = CAUSAL_EST * log_change
ci_lo  = (CAUSAL_EST - 1.96 * CAUSAL_SE) * log_change
ci_hi  = (CAUSAL_EST + 1.96 * CAUSAL_SE) * log_change

col1, col2, col3 = st.columns(3)
col1.metric("Point estimate (pp)", f"{effect:+.3f}")
col2.metric("95% CI lower (pp)",   f"{ci_lo:+.3f}")
col3.metric("95% CI upper (pp)",   f"{ci_hi:+.3f}")

st.info(
    f"A **{mw_change_pct}% increase** in the real minimum wage is estimated to change "
    f"the state unemployment rate by **{effect:+.3f} pp** "
    f"(95% CI: [{ci_lo:+.3f}, {ci_hi:+.3f}])."
)

# ── WHAT-IF CURVE ───────────────────────────────────────────────────────────
pcts   = np.arange(1, 51)
lcs    = np.log(1 + pcts / 100)
effs   = CAUSAL_EST * lcs
lo_arr = (CAUSAL_EST - 1.96 * CAUSAL_SE) * lcs
hi_arr = (CAUSAL_EST + 1.96 * CAUSAL_SE) * lcs

fig = go.Figure()

# 95% CI band
fig.add_trace(go.Scatter(
    x=pcts, y=hi_arr, mode="lines",
    line=dict(width=0), showlegend=False
))
fig.add_trace(go.Scatter(
    x=pcts, y=lo_arr, mode="lines",
    line=dict(width=0),
    fill="tonexty", fillcolor="rgba(24,95,165,0.15)",
    name="95% CI"
))

# Causal estimate line
fig.add_trace(go.Scatter(
    x=pcts, y=effs, mode="lines",
    line=dict(color="#185FA5", width=2.5),
    name="Causal estimate (TWFE DiD)"
))

# Naive OLS line
fig.add_trace(go.Scatter(
    x=pcts, y=NAIVE_EST * lcs, mode="lines",
    line=dict(color="#888780", width=1.5, dash="dot"),
    name="Naive OLS (biased)"
))

# Slider position marker
fig.add_vline(
    x=mw_change_pct, line_dash="dash", line_color="#D85A30",
    annotation_text=f"Selected: {mw_change_pct}%",
    annotation_position="top right"
)

# Zero line
fig.add_hline(y=0, line_width=0.8, line_color="black", opacity=0.3)

fig.update_layout(
    title="Estimated effect of MW increase on state unemployment rate",
    xaxis_title="Minimum wage increase (%)",
    yaxis_title="Estimated change in unemployment rate (pp)",
    template="plotly_white",
    legend=dict(x=0.01, y=0.99),
    margin=dict(t=50, b=40)
)
st.plotly_chart(fig, use_container_width=True)

# ── IDENTIFICATION STRATEGY TABLE ───────────────────────────────────────────
st.subheader("Identification strategy")
st.markdown("""
| Element | Details |
|---|---|
| **Design** | Staggered DiD — 30+ states raised MW above federal floor at different times |
| **Treatment variable** | Log real state minimum wage (deflated by CPI, base year 2000) |
| **Outcome variable** | State unemployment rate (FRED LAUS, seasonally adjusted) |
| **State fixed effects** | Absorb time-invariant confounders: cost of living, industrial mix, union density |
| **Quarter fixed effects** | Absorb common national shocks: recessions, federal policy changes |
| **SE clustering** | State level — accounts for serial correlation within states |
| **Key assumption** | Parallel trends: treated and control states shared the same unemployment trajectory before each hike |
| **Primary threat** | Staggered treatment heterogeneity — TWFE uses already-treated states as controls, potentially with negative weights (Goodman-Bacon 2021) |
| **Robustness checks** | (1) Drop recession quarters 2008Q3–2010Q2; (2) Binary above-federal-floor dummy |
""")

# ── BIAS EXPLAINER ───────────────────────────────────────────────────────────
st.subheader("Why the naive estimate is biased")
st.markdown("""
Pooled OLS without fixed effects conflates the causal effect of wage hikes with **selection bias**:
states that raise their minimum wage (CA, WA, NY, MA) are also wealthier states with structurally
lower unemployment. This creates a spurious negative correlation between wages and unemployment —
attenuating the naive estimate toward zero, or even reversing its sign.

The TWFE DiD strips this out by using **within-state variation over time**: each state's
unemployment after its own hike, compared to before, relative to states that had not yet hiked.
The gap between the naive and causal estimates (shown as the dashed vs. solid lines above)
is a direct visualization of this confounding.
""")
