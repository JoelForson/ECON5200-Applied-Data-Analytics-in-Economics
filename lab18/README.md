## Fraud Detection Model Evaluation — Metrics that Matter

**Objective:** Diagnose the failure modes of accuracy-optimized classification on a
severely imbalanced real-world dataset by constructing a full evaluation framework
spanning confusion matrices, threshold analysis, and business-constrained operating
point selection for a logistic regression fraud detector.

---

### Methodology

- Established the accuracy paradox as a quantitative baseline: a naive all-negative
  classifier achieves 99.83% accuracy on the Kaggle Credit Card Fraud dataset by
  never predicting a single fraud case, exposing accuracy as a misleading metric
  when the positive class represents only 0.172% of 284,807 transactions
- Engineered a complete binary classification evaluation suite using `scikit-learn`,
  including confusion matrix decomposition (TP, FP, TN, FN), `classification_report`
  for Precision, Recall, and F1-Score, and `roc_auc_score` for threshold-independent
  discriminative performance measurement
- Generated and interpreted the ROC curve (TPR vs FPR) and Precision-Recall curve
  simultaneously, using PR-AUC as the primary performance metric given its sensitivity
  to minority class performance in imbalanced regimes where ROC-AUC can be optimistic
- Conducted threshold analysis by sweeping the classification boundary away from the
  default 0.5 and computing F1-Score at each candidate threshold to identify the
  operating point that maximizes the harmonic mean of Precision and Recall on the
  fraud class
- Applied a real-world capacity constraint of 500 maximum daily fraud investigations
  to select a business-relevant threshold, translating model output probabilities into
  an operationally feasible decision rule that balances fraud capture rate against
  analyst workload

---

### Key Findings

The accuracy paradox was confirmed quantitatively: a zero-rule baseline achieved
99.83% accuracy while capturing zero fraud cases, establishing that accuracy is not
a valid optimization target for this problem. Logistic regression trained on
PCA-anonymized features V1–V28 and transaction Amount achieved strong ROC-AUC,
reflecting robust rank-ordering of fraud probability across the full threshold range.
PR-AUC on the fraud class confirmed meaningful signal extraction despite the extreme
class imbalance. Threshold analysis revealed that the F1-optimal decision boundary
differs substantially from the default 0.5 cutoff — shifting the threshold toward
lower probability values recovers a significant fraction of fraud cases at the cost
of acceptable precision loss. The capacity-constrained operating point demonstrated
that business rules, not model defaults, should govern final threshold selection:
at 500 daily investigations, the model captures a materially higher fraud volume
than the default threshold while remaining within operational review capacity.

---

**Tech Stack:** Python · scikit-learn · matplotlib · seaborn · pandas · numpy  
**Data:** Kaggle Credit Card Fraud Detection (284,807 transactions, 0.172% fraud rate)