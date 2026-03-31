# The Cost of Living Crisis: A Data-Driven Analysis

### Quantifying Why the "Average" CPI Fails Students

---

## The Problem: When National Averages Mask Individual Realities

The Consumer Price Index (CPI) is the Federal Reserve's primary inflation gauge, influencing everything from Social Security adjustments to monetary policy. But there's a fundamental flaw: **CPI measures the "average" American household, not specific demographic segments.**

For college students, this creates a dangerous blind spot. While policymakers debate whether inflation is "transitory" based on national CPI trends, students face a materially different economic reality driven by:

- **Housing costs** concentrated in university markets (not suburban homeownership)
- **Tuition inflation** disconnected from general price movements
- **Food delivery services** (Chipotle, DoorDash) replacing home-cooked meals
- **Subscription services** (Spotify, streaming) representing discretionary spending patterns unique to Gen Z

**The research question:** How much does a student-specific price index diverge from official CPI, and what does this reveal about compositional bias in aggregate economic indicators?

---

## Methodology: Building a Custom Student Price Index (SPI)

### Data Architecture

- **Primary Source:** FRED API (Federal Reserve Economic Data)
  - National CPI-U: `CPIAUCSL` (All Urban Consumers, Seasonally Adjusted)
  - Boston Regional CPI: `CUURA103SA0` (Monthly, Not Seasonally Adjusted)
- **Custom Student Basket Components:**
  - Tuition (proprietary institutional data)
  - Rent (regional housing indices)
  - Chipotle prices (corporate earnings data)
  - Spotify subscription costs (historical pricing archives)

### Index Theory: Laspeyres Fixed-Weight Approach

The Student SPI employs a **Laspeyres price index**, the same methodology used by the Bureau of Labor Statistics:
```
SPI_t = (Σ[P_t × Q_0] / Σ[P_0 × Q_0]) × 100
```

Where:
- **P_t** = Current period prices
- **Q_0** = Base period (2016) quantities (fixed basket weights)
- **Base Year:** January 1, 2016 = 100

**Critical Methodological Decision:** All component indices were **re-indexed to January 1, 2016 = 100** before aggregation. This is essential because comparing raw indices with different base years creates incompatible measurements—like using two rulers with different zero marks.

### Base Year Normalization: A Cautionary Tale

**The Problem with Raw Index Comparisons:**  

In preliminary analysis, I initially compared raw tuition data (1982 base = 100) against raw streaming data (1997 base = 100). This created a visual illusion where tuition appeared 10× larger than streaming (~900 vs. ~600 in 2026), but this was merely an artifact of different baseline anchors, not actual relative costs.

<img width="1389" height="690" alt="image" src="https://github.com/user-attachments/assets/3ebc90b0-8897-43ef-b5f8-e7257656bbd9" />


**The Solution:**  

All series were normalized using:
```python
Normalized_Index_t = (Raw_Index_t / Raw_Index_2016) × 100
```

**2016 Baseline Values (Before Normalization):**
- CPI: 237.652
- Tuition: 699.997
- Rent: 291.700
- Spotify: 427.538
- Chipotle: 259.958

After normalization, all series start at 100 in January 2016, making growth rates directly comparable. **This is fundamental to sound index construction and a common pitfall in economic analysis.**

### Weight Allocation (Student-Specific Consumption Basket)

Based on typical undergraduate spending patterns, the Student SPI uses the following weights:
```python
weights = {
    'tuition': 0.35,    # 35% - Largest single expense
    'rent': 0.30,       # 30% - Housing costs
    'chipotle': 0.25,   # 25% - Food/dining (convenience premium)
    'spotify': 0.10     # 10% - Entertainment/subscriptions
}
```

**Rationale for Weight Selection:**
- **Tuition (35%):** Largest fixed cost for full-time students, though varies by institution type
- **Rent (30%):** Second-largest expense, reflecting off-campus housing or dorm costs
- **Food/Chipotle (25%):** Intentionally over-weighted vs. CPI food basket (13%) to capture Gen Z dining patterns—frequent restaurant/delivery usage vs. home cooking
- **Streaming/Spotify (10%):** Captures subscription economy burden (Netflix, Spotify, etc.)

**Note:** This differs from official CPI weights where housing is ~33%, food is ~13%, and education is ~3%. The Student SPI deliberately overweights education and food delivery to reflect actual student consumption.

### Technical Implementation

- **Language:** Python 3.x
- **Libraries:** `pandas`, `fredapi`, `matplotlib`
- **Missing Data Handling:** Forward-fill for bimonthly Boston CPI gaps
- **Re-indexing:** Normalized all series to Jan 2016 = 100 for cross-series comparison

---

## Key Findings: A 4.90 Percentage Point Inflation Gap

<img width="1389" height="690" alt="image" src="https://github.com/user-attachments/assets/c14f375b-7c80-43be-a087-78b0fac5127d" />


### Finding 1: Students Experience Nearly 5% Higher Inflation

My analysis reveals a **+4.90 percentage point divergence** between Student SPI and National CPI as of late 2025:
```
📊 INFLATION GAP: 4.90 percentage points
Student SPI: 142.09 (42.09% cumulative inflation)
Official CPI: 137.19 (37.19% cumulative inflation)

Your costs grew 4.90% FASTER than the government reports!
```

**Interpretation:** Students experienced **13% more inflation** than the "average" American over this 9-year period (4.90 ÷ 37.19 = 13.2% excess burden).

### Finding 2: Boston Actually Runs Cooler Than National Average

<img width="1189" height="690" alt="image" src="https://github.com/user-attachments/assets/c30e6227-abb2-46a4-87dc-0df0009557c7" />

Contrary to expectations about expensive coastal cities, the Boston-Cambridge-Newton regional CPI runs **below** national CPI:

- **National CPI (2025):** 137.19
- **Boston CPI (2025):** 135.25
- **Student SPI (2025):** 142.09
- **Boston Discount:** -1.93 points
- **Student Burden:** +4.90 points

**Implication:** The student inflation gap is **not** driven by geographic location (Boston vs. national). Even students in "cheaper" regions experience the 4.90-point burden because it's **basket composition**, not geography, that matters.

This finding contradicts the common narrative that "student costs are high because they live in expensive cities." The data shows students in Boston face a 4.90-point gap despite Boston's below-average regional inflation. The three-line comparison reveals:
- Grey (National CPI) and Blue (Boston CPI) track closely together
- Red (Student SPI) diverges consistently upward, especially post-2022

### Finding 3: Component-Level Analysis Reveals Drivers

<img width="1389" height="690" alt="image" src="https://github.com/user-attachments/assets/6ecfbf42-6cf7-44ba-a428-7793b8ac25db" />


Decomposing the Student SPI into constituent parts identifies inflation leaders:

| **Component** | **2026 Index** | **Cumulative Inflation** | **Annual Growth Rate** | **Weight in SPI** |
|--------------|----------------|-------------------------|------------------------|-------------------|
| **Rent** | ~152 | +52% | ~4.3%/year | 30% |
| **Chipotle** | ~141 | +41% | ~3.5%/year | 25% |
| **Spotify** | ~140 | +40% | ~3.4%/year | 10% |
| **National CPI** | 137 | +37% | ~3.2%/year | — |
| **Tuition** | ~129 | +29% | ~2.6%/year | 35% |

**Critical Insights:**

1. **Rent is the primary driver** of Student SPI divergence (+52% vs. +37% CPI), reflecting housing crises in university markets. With a 30% weight, rent alone contributes **~4.5 percentage points** of excess inflation.

2. **Tuition grew slower than CPI** during this period (+29% vs. +37%)—challenging conventional wisdom about "runaway tuition costs." However, this doesn't mean college is more affordable; it reflects:
   - Institutional tuition freezes during pandemic
   - Shift toward public universities in sample data
   - Does NOT account for reduced financial aid or fee increases

3. **Behavioral consumption patterns matter:** Food delivery (Chipotle +41%) inflated faster than general food prices, reflecting Gen Z convenience preferences. With a 25% weight (vs. CPI's 13% food allocation), this structural difference drives sustained divergence.

4. **Subscription creep:** Streaming services (+40%) outpaced general entertainment inflation, capturing the "death by a thousand subscriptions" phenomenon affecting Gen Z budgets.

### Finding 4: The 2020-2021 Pandemic Convergence

Both indices show a sharp convergence in 2020-2021 (visible in Image 3), where the "Student Burden Gap" temporarily narrows from ~6 points to ~2 points. Possible explanations:
- Remote learning reduced housing demand (rent deflation in college towns)
- Tuition freezes/discounts by universities responding to crisis
- Reduced discretionary spending (dining, entertainment closed)
- National CPI spiked from pandemic supply chain disruptions while student costs stabilized

**This validates the methodology:** The index correctly captures real economic shocks affecting student-specific consumption patterns.

### Finding 5: Post-Pandemic Divergence Accelerates (2022-2025)

After temporary convergence, the gap **re-expands** from 2 points (2021) to 4.90 points (2025), suggesting:
- Housing markets in college towns recovered faster than national averages
- Return to in-person learning restored pre-pandemic consumption patterns
- Student-specific inflation outpaced general economic recovery
- "Revenge spending" on food delivery and entertainment drove Chipotle/Spotify components higher

The re-widening gap indicates the 2020-2021 convergence was an anomaly, not a structural shift.

---

## Economic Implications

### 1. Policy Blindness: The Real Value Erosion

Federal student aid adjustments (Pell Grants, loan limits) tied to National CPI **systematically understate** true student cost inflation by 4.90 percentage points.

**Practical Impact:**  

If a student received $6,000 in aid in 2016, CPI-adjusted aid in 2025 should be:
- **Using National CPI:** $6,000 × 1.3719 = $8,231
- **Using Student SPI:** $6,000 × 1.4209 = $8,525
- **Shortfall:** $294/year per student

Multiplied across **~20 million college students**, this represents approximately **$5.9 billion in uncompensated annual cost increases** systemwide.

### 2. Labor Market Distortions

If students experience 42% inflation but minimum wages rise with CPI at 37%, the real wage gap for student workers **erodes by 5 percentage points**, potentially driving:
- Increased reliance on student loans (+5% real value loss annually)
- Higher working hours (25-30 hrs/week becoming necessary, reducing study time)
- Delayed graduation rates (students dropping to part-time status)

### 3. Compositional Bias in Aggregate Indices

This analysis demonstrates a fundamental limitation of Laspeyres indices: **aggregation across heterogeneous populations masks distributional effects.** The "average" household CPI systematically understates inflation for:

| **Demographic** | **Why CPI Understates Their Inflation** |
|----------------|------------------------------------------|
| Young renters | Rent +52% vs. homeowner mortgage (fixed) |
| Urban populations | Concentration in high-cost metro areas |
| Service consumers | Services inflated faster than goods post-2020 |
| Students | High food delivery/subscription usage vs. CPI weights |

### 4. The Tuition Paradox

The finding that tuition (+29%) grew **slower** than CPI (+37%) contradicts popular narratives. Possible explanations:
- Increased competition from online education (pandemic acceleration)
- State funding interventions (tuition freezes in public systems)
- Mix shift toward public vs. private institutions in enrollment data
- **Critical caveat:** My tuition index reflects sticker prices, not net costs. Financial aid reductions could offset sticker price freezes, meaning students pay more out-of-pocket despite slower headline tuition growth.

This warrants further investigation with net-price data (sticker minus aid), but highlights the danger of anecdotal evidence overriding empirical analysis.

---

## Methodological Lessons Learned

### 1. Base Year Consistency is Non-Negotiable

The most important technical insight from this project: **never compare raw indices with different base years**. Initial analysis (Image 2) showed "tuition at 900" vs. "streaming at 600," implying tuition was 1.5× higher. After proper normalization to 2016=100, both inflated similarly (~29% vs. ~40%), completely changing the interpretation.

**This is a foundational error in economic analysis** that I caught through data visualization—the raw index chart looked "wrong," prompting methodological review.

### 2. Weight Selection Requires Domain Knowledge

Using **35% tuition, 30% rent, 25% food, 10% streaming** better captures student reality than CPI's housing-dominant weights. This required:
- Literature review of student budget studies
- Understanding of Gen Z consumption patterns (high food delivery usage)
- Recognition that students don't purchase cars, healthcare, or durables at CPI rates

**Lesson:** Index construction is part art, part science—weights should reflect actual behavior, not just mathematical convenience.

### 3. Forward-Fill for Frequency Mismatches

Boston CPI data arrived at bimonthly frequency while other series were monthly/annual. Forward-filling preserves the last-known value until new data arrives—appropriate for slow-moving economic indicators but potentially problematic for volatile series.

**Alternative considered:** Linear interpolation, but rejected because it creates artificial smoothing that doesn't reflect true price stickiness.

### 4. Visualization Choices Shape Narrative

Image 3's shaded "Student Burden Gap" makes the divergence visceral in ways raw numbers cannot. The 4.90-point gap appears modest in a table but the visual reveals:
- Persistent divergence (not just a one-time shock)
- Widening post-pandemic (gap is growing, not stabilizing)
- Scale of burden relative to baseline (gap is ~13% of total inflation)

---

## Technical Execution Highlights

✅ **API Integration:** Automated FRED data retrieval using `fredapi` for reproducible research  
✅ **Index Theory Application:** Implemented Laspeyres methodology from first principles with proper base-year normalization  
✅ **Data Wrangling:** Handled mixed-frequency time series (monthly/annual) with forward-fill interpolation  
✅ **Methodological Rigor:** Identified and corrected base-year comparison errors through visualization—demonstrating statistical maturity  
✅ **Weight Calibration:** Custom basket weights (35/30/25/10) based on student consumption patterns, not CPI defaults  
✅ **Visualization Design:** Created 4 complementary charts telling a coherent narrative from multiple angles  
✅ **Economic Intuition:** Translated statistical findings into policy-relevant insights with real-world dollar impact calculations  

---

## Reflection: Bridging Theory and Practice

This project exemplifies my approach to applied economics: **start with theory (index construction), operationalize with modern tools (Python/APIs), validate through data (base year corrections), and communicate findings accessibly (visualizations + narrative).**

The Student SPI analysis demonstrates how custom indices can reveal blind spots in standard macroeconomic indicators—a skill directly applicable to roles in:

- **Economic Consulting:** Building client-specific cost indices for contract negotiations (e.g., wage indexing for teacher unions)
- **Central Banking:** Understanding demographic-specific inflation for targeted monetary policy (avoiding one-size-fits-all rate decisions)
- **Fintech:** Designing affordability algorithms that reflect actual user cost burdens, not national averages (e.g., student loan servicers, budgeting apps)
- **Policy Analysis:** Quantifying distributional impacts of inflation for evidence-based legislative design

**Key Takeaway:** The 4.90-point gap isn't just a statistical curiosity—it represents **$5.9 billion in annual uncompensated costs**, real financial hardship, policy failures, and the limitations of one-size-fits-all economic measurement. Data science isn't just about building models; it's about asking **"whose reality does this number represent?"** and ensuring marginalized perspectives (like students) aren't hidden in national averages.

---

## Future Extensions

### Analytical Depth:
1. **Geographic Decomposition:** Compare Student SPI across Boston, San Francisco, rural college towns to test whether the 4.90-point gap holds nationally or varies by region
2. **Substitution Effects:** Build a Tornqvist index to capture behavioral changes (students switching to ramen when Chipotle inflates, or canceling Spotify)
3. **Predictive Modeling:** ARIMA/Prophet time series forecasting to project when Student SPI hits 150 (50% inflation threshold) and what policy interventions could prevent it

### Data Enhancements:
4. **Net Price Analysis:** Incorporate financial aid data to measure true out-of-pocket tuition costs vs. sticker prices
5. **Granular Components:** Break down "rent" into on-campus dorms vs. off-campus apartments, "food" into groceries vs. dining hall vs. delivery
6. **Income Integration:** Cross-reference with student earnings data to calculate real wage erosion (inflation-adjusted purchasing power)

### Policy Applications:
7. **Aid Indexing Simulation:** Model impact of switching Pell Grants from CPI-indexed to SPI-indexed on debt burdens and graduation rates
8. **Regional Adjustments:** Propose differential aid formulas based on local Student SPI calculations (Boston students get +4.90% vs. rural students)
9. **Legislative Brief:** Package findings into policy memo for Congressional education committees

---

## Tools & Skills

**Tools Used:** Python • pandas • fredapi • matplotlib • Economic Theory (Laspeyres Index) • FRED API  
**Skills Demonstrated:** Data Pipeline Construction • API Integration • Time Series Analysis • Data Visualization • Economic Policy Analysis • Methodological Critique • Index Construction
---

*© 2025 Joel Aryee | Business Analytics & MIS | Northeastern University*
