# Replication Study: Card & Krueger (1994) 

**Track:** Labor Economics / Program Evaluation  
**Paper:** Card, D., & Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American Economic Review, 84*(4), 772–793.  
---

##  Summary

Card and Krueger ask whether a minimum wage increase causes a reduction in employment, they make a prediction of standard competitive labor market theory. To answer this, they run a natural experiment: New Jersey raised its minimum wage from $4.25 to $5.05 in April 1992, while neighboring Pennsylvania held its wage constant, allowing the authors to use a Difference-in-Differences design comparing fast-food employment across both states before and after the policy change. Contrary to the standard prediction, they find that employment in New Jersey in fact *increased* relative to Pennsylvania after the wage hike, challenging the textbook view and igniting one of the most influential debates in modern labor economics.
---
# Policy Memo: The Employment Effects of Minimum Wage Legislation
**To:** Executive Policy Board
**From:** Joel Forson, Senior Data Economist
**Re:** Replication and Extension of Card & Krueger (1994)
**Date:** March 2026

---

## The Bottom Line Up Front

New Jersey's 1992 minimum wage increase from $4.25 to $5.05 did not reduce fast-food
employment, contradicting the standard economic prediction that higher wages destroy
jobs. More importantly, this analysis extends that finding by showing the employment
effect was not uniform across all restaurants, it was concentrated specifically in
stores where workers were genuinely earning below the new wage floor before the law
changed.

---

## The Mechanism: How We Simulated a Randomized Experiment

Isolating the true effect of a policy is difficult because many things change at once.
The reason this study is credible is that New Jersey and Pennsylvania are neighboring
states with nearly identical fast-food industries, and only New Jersey raised its
minimum wage in April 1992. Pennsylvania, doing nothing different, serves as the
control group.

Think of it like a natural experiment in a hospital: if two wards have identical
patients but only one ward receives a new treatment, any difference in outcomes
between the wards at the end of the study can be attributed to the treatment itself,
not to pre-existing differences between patients. Here, the "patients" are fast-food
restaurants, the "treatment" is the wage hike, and the "outcome" is employment levels
before and after the law took effect.

This approach is called Difference-in-Differences (DiD). It compares how much
employment changed in New Jersey, then subtracts how much employment changed in
Pennsylvania over the same period. Whatever is left after that subtraction is the
causal effect of the policy, because both states experienced the same national economy,
the same consumer trends, and the same industry conditions in 1992. The only thing
that was different was the minimum wage.

---

## The Visual Evidence

<img width="1089" height="790" alt="image" src="https://github.com/user-attachments/assets/6c6c87d7-c23c-43f7-a760-4a6374775400" />


**Figure 1. Heterogeneous Treatment Effects, Card & Krueger (1994) Extension.**
Each row shows the estimated employment effect (DiD coefficient) for two subgroups
defined by a store characteristic, with 95% confidence intervals shown as horizontal
lines. Blue circles represent the baseline group (moderator = 0) and red squares
represent the comparison group (moderator = 1). The orange dotted line marks the
aggregate baseline DiD estimate for reference. A ★ denotes interactions where the
difference between the two groups is statistically significant at the 5% level.
The two significant results, AT_FLOOR and HIGH_PCTAFF, confirm that the employment
effect was driven by stores where the wage mandate was genuinely binding.

---

## Business and Policy Implications

**For policymakers considering minimum wage legislation:**
The evidence does not support the fear that wage floors universally destroy jobs.
Employment effects depend entirely on how many workers in a given market are actually
earning below the proposed floor before the law takes effect. A wage increase set well
above prevailing market wages will behave very differently from one calibrated to the
lower end of the existing distribution. Policymakers should audit the wage distribution
in target industries before setting the floor, not after.

**For businesses operating near the wage floor:**
Stores already paying above the minimum wage showed no statistically significant
employment disruption. The adjustment cost falls almost entirely on low-wage operators.
Companies in this position should treat compliance planning, including scheduling
optimization and pricing adjustments, as a near-term operational priority rather than
a long-term strategic threat.

**For labor advocates and unions:**
The dose-response finding supports a targeted approach to wage advocacy. The workers
who benefited most were those in stores where the largest fraction of the workforce was
directly affected by the mandate. Campaigns focused on industries and regions with
high concentrations of sub-floor earners will produce larger and more measurable
employment gains than broad economy-wide increases applied uniformly across markets
with already-elevated wage levels.

**The bottom line for all stakeholders:** minimum wage policy works differently
depending on where you sit relative to the floor. The policy does not hurt everyone,
and it does not help everyone equally. The data tells you exactly where the effects
concentrate, and that information should drive every decision made on both sides of
the debate.

---

## Data Source

- **File:** `data/raw/public.dat`
- **Source:** [David Card's UC Berkeley data page](https://davidcard.berkeley.edu/data_sets.html)
- **Format:** Space-delimited text, 410 fast-food restaurant observations (Burger King, KFC, Wendy's, Roy Rogers)
- **Coverage:** Two survey waves — Wave 1 (Feb/Mar 1992, *before* NJ increase) and Wave 2 (Nov/Dec 1992, *after* NJ increase)


The goal is to analyze and recreate the observation that NJ restaurants increased FTE employment by ~2.76 jobs *more* than PA restaurants after the minimum wage increase

---

## References

Card, D., & Krueger, A. B. (1994). Minimum wages and employment: A case study of the fast-food industry in New Jersey and Pennsylvania. *American Economic Review, 84*(4), 772–793.
