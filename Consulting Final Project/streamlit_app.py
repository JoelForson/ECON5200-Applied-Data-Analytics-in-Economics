app_code = '''
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MW DiD Dashboard", layout="wide")
st.title("Minimum Wage & Unemployment: Causal Effect Dashboard")
st.markdown("""
**Causal question:** Does raising the state minimum wage increase unemployment?  
**Method:** Two-Way Fixed Effects Difference-in-Differences (state + quarter FE)  
**Data:** FRED LAUS + DOL minimum wage, 50 states, 2000–2022
""")

# --- Inputs: paste your fitted estimates here ---
CAUSAL_EST = 0.0    # TODO: replace with your res_twfe.params['log_mw_real']
CAUSAL_SE  = 0.0    # TODO: replace with your res_twfe.std_errors['log_mw_real']
NAIVE_EST  = 0.0    # TODO: replace with your naive_est

st.sidebar.header("What-if scenario")
mw_change_pct = st.sidebar.slider(
    "Minimum wage increase (%)", min_value=1, max_value=50, value=10, step=1
)

# Compute what-if effect
# β = effect of 1 unit increase in log(MW); 10% increase = log(1.10) ≈ 0.0953
log_change = np.log(1 + mw_change_pct / 100)
effect     = CAUSAL_EST * log_change
ci_lo      = (CAUSAL_EST - 1.96 * CAUSAL_SE) * log_change
ci_hi      = (CAUSAL_EST + 1.96 * CAUSAL_SE) * log_change

col1, col2, col3 = st.columns(3)
col1.metric("Estimated effect on unemployment", f"{effect:+.3f} pp")
col2.metric("95% CI lower", f"{ci_lo:+.3f} pp")
col3.metric("95% CI upper", f"{ci_hi:+.3f} pp")

st.markdown(f"""
> A **{mw_change_pct}% increase** in the real minimum wage is estimated to change
> the unemployment rate by **{effect:+.3f} percentage points** (95% CI: [{ci_lo:+.3f}, {ci_hi:+.3f}]).
""")

# What-if curve
pcts   = np.arange(1, 51)
lcs    = np.log(1 + pcts / 100)
effs   = CAUSAL_EST * lcs
lo_arr = (CAUSAL_EST - 1.96 * CAUSAL_SE) * lcs
hi_arr = (CAUSAL_EST + 1.96 * CAUSAL_SE) * lcs

fig = go.Figure()
fig.add_trace(go.Scatter(x=pcts, y=hi_arr, mode="lines", line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=pcts, y=lo_arr, mode="lines", line=dict(width=0),
                         fill="tonexty", fillcolor="rgba(24,95,165,0.15)", name="95% CI"))
fig.add_trace(go.Scatter(x=pcts, y=effs, mode="lines",
                         line=dict(color="#185FA5", width=2.5), name="Causal estimate (TWFE)"))
fig.add_trace(go.Scatter(x=pcts, y=NAIVE_EST * lcs, mode="lines",
                         line=dict(color="#888780", width=1.5, dash="dot"), name="Naive OLS"))
fig.add_vline(x=mw_change_pct, line_dash="dash", line_color="#D85A30",
              annotation_text=f"{mw_change_pct}%")
fig.add_hline(y=0, line_width=0.8, line_color="black", opacity=0.4)
fig.update_layout(
    title="What-if: effect of MW increase on unemployment",
    xaxis_title="Minimum wage increase (%)",
    yaxis_title="Estimated change in unemployment rate (pp)",
    template="plotly_white", legend=dict(x=0.01, y=0.99)
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Identification strategy")
st.markdown("""
| Element | Details |
|---|---|
| **Design** | Staggered DiD — states treated at different times |
| **Fixed effects** | State FE (absorbs time-invariant confounders) + Quarter FE (absorbs national trends) |
| **SE clustering** | State level (Bertrand, Duflo & Mullainathan 2004) |
| **Key assumption** | Parallel trends — visually supported by pre-trend plot |
| **Threat** | Staggered heterogeneity bias — Callaway-Sant'Anna (2021) as robustness |
""")
'''

with open('app.py', 'w') as f:
    f.write(app_code)
print('app.py written. Deploy to https://streamlit.io/cloud')
