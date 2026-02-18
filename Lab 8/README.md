# Hypothesis Testing & Causal Evidence Architecture

**The Epistemology of Falsification: Hypothesis Testing on the Lalonde Dataset**

---

## Objective

Most analytical pipelines are optimized for *estimation* — producing a number. This project reorients that workflow toward *falsification*: the harder, more scientifically rigorous question of whether a measured effect is real or statistical noise. Using the Lalonde (1986) dataset — a canonical benchmark in causal inference — I operationalized the scientific method to adjudicate between competing narratives of causality around the Average Treatment Effect (ATE) of job training programs on real earnings.

---

## Technical Approach

The analysis was structured as a two-stage hypothesis testing framework, implemented in Python via `scipy.stats`:

- **Parametric Testing (Welch's T-Test):** Computed the signal-to-noise ratio between treatment and control groups without assuming equal population variances — a deliberate choice given the heterogeneous labor market profiles in the Lalonde sample. This produced the primary ATE estimate and a p-value used to evaluate the Null Hypothesis under normality assumptions.

- **Non-Parametric Validation (Permutation Test, n=10,000 resamples):** To stress-test the parametric result against the non-normal earnings distributions characteristic of real-world wage data, I constructed an empirical null distribution through random label shuffling. This bootstrap-style approach confirmed result robustness without distributional assumptions.

- **Type I Error Control:** Both tests were evaluated against a pre-specified significance threshold (α = 0.05), enforcing a disciplined decision boundary and guarding against false positives introduced by analyst discretion or opportunistic p-value interpretation.

---

## Key Findings

The analysis identified a statistically significant lift in real earnings of approximately **$1,795** attributable to job training participation. The Null Hypothesis — that the program produced no measurable effect — was rejected via *Proof by Statistical Contradiction* across both the parametric and non-parametric frameworks, providing convergent evidence of a genuine treatment signal.

---

## Business Insight: Hypothesis Testing as the Safety Valve of the Algorithmic Economy

In an environment where data is abundant and models are cheap to run, the costliest failure mode is not *underfitting* — it's *overclaiming*. Data grubbing, p-hacking, and spurious correlations are not fringe concerns; they are the predictable output of optimization pipelines that lack a falsification discipline.

Rigorous hypothesis testing functions as the **safety valve** of this system. By forcing analysts to specify a Null before observing results, construct a valid counterfactual, and survive a pre-defined rejection threshold, it transforms statistical output from a narrative tool into an evidentiary standard. For decision-makers downstream — whether allocating program funding, deploying a pricing model, or scaling an intervention — the difference between a *significant* result and a *defensible* one is the difference between a recommendation and a liability.

This project treats that distinction seriously.
