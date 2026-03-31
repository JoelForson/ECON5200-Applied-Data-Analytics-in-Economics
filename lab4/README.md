# Anomaly Detection in Housing Markets: The Pareto World

### Uncovering the "Elon Musk Effect" in California Real Estate Data

---

## The Problem: When Outliers Tell the Real Story

Traditional statistical analysis assumes normal distributions—but housing markets exhibit **extreme right-skewness** where ultra-high-value properties distort aggregate statistics. This project tackles: **How do we systematically identify and analyze anomalous housing markets without discarding valuable signal as "noise"?**

The California Housing dataset presents three challenges:
1. **The $500k Ceiling Effect**: Artificial truncation at $500,000 (1990 dollars)
2. **The Wealth Tail**: High-income districts (Palo Alto, Beverly Hills) with fundamentally different dynamics
3. **Measurement Error**: Extreme values (15+ rooms) may represent data quality issues vs. genuine mansions

**Goal:** Build a robust outlier detection framework distinguishing between legitimate extremes, data anomalies, and structural breaks.

---

## Methodology: IQR vs. Machine Learning Detection

### Two-Stage Framework

#### Stage 1: Classical IQR (Tukey Fence)
```
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```
**Result:** 681 outliers (3.3% of data)  
**Limitation:** Only examines one variable at a time

#### Stage 2: Isolation Forest (Algorithmic Detection)

Isolation Forest detects anomalies by measuring how quickly a point can be "isolated" through random partitioning. Outliers require fewer splits.
```python
iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population']
predictions = iso_forest.fit_predict(df[features])
```

**Result:** 1,032 outliers (5.0%)  
**Advantage:** Captures multivariate patterns—unusual *combinations* of features

---

## Key Findings

### Finding 1: Algorithmic Detection Captures 52% More Outliers

- **Manual IQR:** 681 outliers (3.3%)
- **Isolation Forest:** 1,032 outliers (5.0%)
- **Gap:** 351 additional outliers represent **multivariate anomalies**

Districts that don't look unusual individually but exhibit strange feature combinations (e.g., high income + mansion-sized homes).

### Finding 2: The $500k Ceiling Effect
```
MedHouseVal Statistics:
Mean:    $206,856
Median:  $179,700
Max:     $500,010 ← Artificial cap
```

Properties above $500k are **censored**, creating right-truncation bias affecting mean calculations, regression models, and inequality metrics.

### Finding 3: The Inequality Wedge Reveals Two Worlds

**Inequality Wedge = Mean - Median** (measures right-skewness)

| **Metric** | **Normal Districts** | **Outlier Districts** | **Ratio** |
|-----------|---------------------|----------------------|-----------|
| **Income Mean** | $37,696 | $57,908 | 1.54× |
| **Income Median** | $35,156 | $42,570 | 1.21× |
| **Inequality Wedge** | $2,540 | $15,338 | **6.04×** |

**Critical Insight:** Outlier districts have a **6× larger inequality wedge**, indicating extreme internal wealth stratification—not just "rich neighborhoods" but places with concentrated ultra-wealth.

### Finding 4: Volatility Metrics - Standard Deviation vs. MAD

| **Group** | **Income Std Dev** | **Income MAD** | **SD/MAD Ratio** |
|----------|-------------------|---------------|------------------|
| Normal | $16,406 | $10,317 | 1.59 |
| Outliers | $41,454 | $24,919 | **1.66** |

**MAD (Median Absolute Deviation):** Robust to extremes  
**SD/MAD > 1.5:** Extreme values driving volatility—the **"Elon Musk Effect"** where one billionaire doubles zip code standard deviation.

### Finding 5: Three Distinct Clusters

Scatter plot reveals:
1. **Core Market:** Dense concentration around $35k income, 5-6 rooms
2. **Wealth Tail:** High income + large homes (Beverly Hills pattern)
3. **Data Errors:** Low income + excessive rooms (measurement issues)

---

## Economic Implications

### 1. The Pareto Principle: 5% Drive 20% of Market Value
- Outliers average $266k vs. $203k (31% premium)
- 54% higher median income
- 2.5× higher volatility

### 2. Mean vs. Median: Why Averages Lie
In outlier districts, **mean income ($57,908)** overstates typical resident by **36%** vs. median ($42,570). Policies using mean-based thresholds systematically exclude middle-income residents in wealthy areas.

### 3. Censored Data Bias
The $500k cap creates systematic underestimation of wealth inequality, price-to-income ratios in elite markets, and true investment returns.

---

## Methodological Lessons

### 1. Multivariate > Univariate
IQR: 681 outliers | Isolation Forest: 1,032 (+52%)  
**Lesson:** Housing markets depend on feature *combinations*, not isolated variables.

### 2. Robustness Trade-Off
- **SD:** Useful for detecting extremes
- **MAD:** Better for measuring typical spread
- **SD/MAD > 2.0:** Use MAD for policy decisions

### 3. Contamination Parameter
Setting `contamination=0.05` is subjective—validate against domain knowledge and cross-reference with IQR.

### 4. Visualization as Validation
Boxplots and scatter plots confirm outliers cluster coherently at extremes (genuine economic segments) rather than random scatter (data errors).

---

## Technical Execution

✅ **Algorithm Selection:** Isolation Forest for speed and multivariate detection  
✅ **Feature Engineering:** 5 features capturing income, demographics, housing  
✅ **Robust Statistics:** MAD alongside standard deviation  
✅ **Two-Stage Detection:** IQR → Isolation Forest validation  
✅ **Economic Interpretation:** Inequality wedge quantifies skewness  
✅ **Comparative Visualization:** Normal vs. outlier distributions  

---

## Key Takeaway

In economic data science, **outliers aren't nuisances—they're the most interesting observations.** The top 5% of housing markets drive innovation, policy debates, and investment returns. This methodology applies to:

- **Credit Risk:** Detecting fraud vs. legitimate high-earners
- **E-commerce:** VIP customers vs. bots
- **Healthcare:** Rare disease clusters vs. data errors
- **Fraud Detection:** Unusual-but-legitimate vs. criminal activity

The Isolation Forest found anomalies, but the real work was asking **why they're different** and what that reveals about market structure.

---

## Future Extensions

**Analytical:**
1. Geographic clustering to map wealth concentration
2. Regression discontinuity modeling for normal vs. outlier markets
3. SHAP values for explainability

**Data:**
4. Uncensored Zillow/Redfin data to remove $500k cap
5. Add crime, schools, commute times
6. Validate against Forbes "richest zip codes"

**Methodological:**
7. Ensemble methods (Isolation Forest + LOF + One-Class SVM)
8. Hyperparameter tuning via grid search
9. Temporal analysis if time-series available

---

## Tools & Skills

**Tools:** Python • scikit-learn • pandas • seaborn • matplotlib • Isolation Forest • IQR  
**Skills:** Anomaly Detection • Robust Statistics • Data Quality Assessment • EDA • Algorithm Selection • Economic Interpretation

**Dataset:** California Housing (20,640 observations, 8 features)

---

*© 2025 Joel Aryee | Business Analytics & MIS | Northeastern University*
