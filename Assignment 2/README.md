# Audit 02: Deconstructing Statistical Lies

**Role:** Data Quality Auditor, Pareto Ventures  
**Course:** ECON 5200 — Applied Data Analytics  
**Tools:** Python, NumPy, Matplotlib, Pandas

---

## The Mission

Three portfolio companies pitched "perfect" metrics. My job was to find the statistical lie hidden in their averages using manual implementations of core statistical tests — no black-box libraries allowed.

---

## Finding 1: Latency Skew — The Mean is a Vanity Metric

**Company:** NebulaCloud  
**Claim:** "Our mean latency is 35ms."  
**Verdict:** Misleading.

I simulated 1,000 server requests: 980 normal (20–50ms) and 20 catastrophic spikes (1,000–5,000ms). The mean ballooned to ~90ms while the median stayed at ~35ms — a 2.5x gap caused by just 2% of traffic.

To quantify this, I built `calculate_mad(data)` from scratch — a three-line function that computes the Median Absolute Deviation by finding the median, measuring each point's absolute distance from it, then taking the median of those distances. The result: Standard Deviation exploded past 300ms because it squares deviations (amplifying outliers), while MAD held steady near 8ms because the median is immune to extreme tails.

**Takeaway:** In skewed systems, report the median and MAD. The mean and SD are vanity metrics that hide tail risk.

---

## Finding 2: False Positives — The Base Rate Fallacy

**Company:** IntegrityAI  
**Claim:** "Our plagiarism detector is 98% accurate."  
**Verdict:** Dangerously incomplete.

I implemented Bayes' Theorem manually to compute P(Cheater | Flagged) across three base-rate environments:

| Scenario | Base Rate | P(Cheater \| Flagged) |
|---|---|---|
| Bootcamp | 50% | 98.00% |
| Econ Class | 5% | 72.06% |
| Honors Seminar | 0.1% | **4.67%** |

In the Honors Seminar, a flagged student has only a 4.67% chance of actually cheating — meaning ~95 out of 100 flags are false accusations. The 98% accuracy figure collapses when prevalence is low because the false positive rate (2%) generates far more noise than the tiny cheater pool generates signal.

**Takeaway:** Accuracy without base rates is marketing, not science. Always ask: "accurate relative to what prevalence?"

---

## Finding 3: Sample Ratio Mismatch — The Missing 500

**Company:** FinFlash  
**Claim:** "Our A/B test shows a huge win."  
**Verdict:** Split is valid (but the instinct to check was correct).

FinFlash's 50/50 A/B test showed 50,250 Control vs. 49,750 Treatment — 500 users "missing" from Treatment. I performed a manual Chi-Square Goodness of Fit test:

```
χ² = (250²/50,000) + (250²/50,000) = 2.50
Critical value (df=1, α=0.05) = 3.84
2.50 ≤ 3.84 → Fail to reject H₀
```

The 250-user-per-group deviation falls within normal randomization noise. Sensitivity analysis showed the threshold breaks around ±310 users — meaning FinFlash's gap is unremarkable, but a 500-user gap per side (50,500/49,500, χ²=10.0) would invalidate the experiment.

**Takeaway:** Always run SRM checks before trusting A/B results. The Chi-Square test is the gatekeeper.

---

## Finding 4: Survivorship Bias — The Memecoin Graveyard

**Context:** AI-assisted expansion (P.R.I.M.E. framework)

I simulated 10,000 token launches using a Pareto distribution (α=1.05) and split them into two views: the full market ("The Graveyard") and the top 1% ("The Survivors"). The survivors' mean market cap was ~47x higher than the true market average — a distortion created entirely by which subset you choose to display.

This is the same structural illusion that crypto influencers exploit: showcasing winners while 98.6% of tokens quietly die. Analyzing only listed coins is survivorship bias in its purest form.

**Takeaway:** Any dataset that filters on the outcome variable (survival, success, listing) will overestimate performance. Always ask: "where are the dead tokens?"

---

## Key Methodological Principles

1. **Robust statistics (median, MAD) resist outliers; classical statistics (mean, SD) amplify them.** Choose your metric based on your data's shape, not convention.
2. **Conditional probabilities require base rates.** Bayes' Theorem is the correction that transforms "accuracy" into actionable insight.
3. **Pre-analysis integrity checks (SRM) protect against silent engineering failures.** Run them before interpreting any experimental result.
4. **Survivorship bias is invisible by default.** The data you don't see matters more than the data you do.
