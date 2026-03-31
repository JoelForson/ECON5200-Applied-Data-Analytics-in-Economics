# Recovering Experimental Truths via Propensity Score Matching

## Objective
This project demonstrates the application of propensity score matching to correct selection bias in observational data, recovering causal treatment effects that approximate randomized experimental results.

## Methodology
* **Selection Bias Modeling**: Identified and quantified the systematic differences between treatment and control groups in observational data
* **Propensity Score Estimation**: Developed logistic regression models to predict treatment assignment probability based on observed confounders
* **Nearest Neighbor Matching**: Implemented 1:1 matching algorithms with replacement to construct balanced treatment and control groups
* **Effect Estimation**: Applied statistical inference methods to estimate causal effects on the matched sample

## Key Findings
The analysis successfully corrected severe selection bias present in the observational subset of the LaLonde job training dataset:

* **Naive Observational Estimate**: -$15,204 (heavily biased due to selection effects)
* **Recovered Causal Effect**: +$1,800 (closely approximating experimental benchmark)
* **Bias Correction**: Achieved a swing of approximately $17,000 through propensity score matching

This dramatic correction illustrates both the severity of selection bias in observational studies and the effectiveness of propensity score methods in recovering experimental truths when randomization is not feasible.

## Technical Implementation
Built using Python ecosystem tools including Pandas for data manipulation, Scikit-Learn for machine learning components, and SciPy for statistical inference testing.
