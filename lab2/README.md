# The Illusion of Growth & The Composition Effect

## Objective

This project develops an automated Python pipeline to ingest and analyze live economic data from the Federal Reserve Economic Data (FRED) API, investigating long-term wage stagnation in the United States and identifying systematic biases in standard labor market indicators. The analysis demonstrates how compositional changes in the workforce can distort aggregate wage statistics, leading to misleading conclusions about economic prosperity.

---

## Methodology

### Data Acquisition Pipeline

**API Integration & Automation**
- Implemented `fredapi` library to programmatically fetch real-time macroeconomic time series data
- Automated data retrieval eliminates manual updates and ensures reproducibility
- Primary data series accessed:
  - **AHETPI**: Average Hourly Earnings of Production and Nonsupervisory Employees (nominal wages)
  - **CPIAUCSL**: Consumer Price Index for All Urban Consumers (inflation adjustment)
  - **ECIWAG**: Employment Cost Index for Total Compensation (composition-controlled measure)

### Three-Phase Analytical Framework

**Phase 1: Real Wage Calculation**
- Deflated nominal wages using CPI to compute real purchasing power
- Constructed a 50+ year historical time series (1964-present) to assess secular trends
- Identified persistent divergence between nominal growth and real wage stagnation
- Visualization revealed the **Money Illusion**: workers perceive rising pay but experience flat purchasing power

**Phase 2: Anomaly Detection**
- Detected sharp upward spike in real wages during March-April 2020
- Initial hypothesis testing: genuine wage growth vs. statistical artifact
- Temporal analysis showed spike coincided with pandemic-induced labor market disruption

**Phase 3: Composition Effect Correction**
- Retrieved Employment Cost Index (ECI) data to isolate compositional bias
- **Key insight**: ECI holds job mix constant, measuring wage changes for a fixed basket of occupations
- Comparative analysis: standard average wage vs. composition-adjusted ECI
- Divergence between measures confirmed compositional bias hypothesis

---

## Key Findings

### The Money Illusion: Five Decades of Stagnation

The analysis reveals a stark disconnect between nominal and real wage growth spanning 50+ years. While nominal wages have increased substantially, inflation-adjusted purchasing power has remained essentially flat since the early 1970s. This finding underscores a critical distinction in economic analysis: **absolute dollar increases do not equate to improved living standards**.

**Economic Implications:**
- Workers experience the "Money Illusion"—perceiving nominal increases as real gains
- Productivity gains have not translated into proportional wage growth for typical workers
- Policy discussions must distinguish between nominal growth and purchasing power

### The Pandemic Paradox: When Good News Isn't

The 2020 data presented a puzzling anomaly: real wages appeared to surge dramatically during the most severe economic contraction since the Great Depression. Conventional economic theory would suggest wages should decline during recessions, yet the data showed the opposite.

**Root Cause: The Composition Effect**

Deeper investigation revealed the "wage boom" to be entirely artifactual, driven by structural changes in the labor force composition:

**Mechanism:**
1. **Sectoral job losses**: Low-wage sectors (hospitality, retail, food service) experienced disproportionate layoffs
2. **Survivor bias**: The remaining employed population skewed toward higher-wage occupations
3. **Arithmetic artifact**: Average wage rose not because individual workers earned more, but because lower-paid workers dropped out of the calculation

**Validation Through ECI:**

The Employment Cost Index, which controls for occupational shifts, showed **stable, modest growth** during the same period—completely contradicting the apparent "boom" in standard measures. This discrepancy proves the spike was purely compositional.

**Lessons for Economic Analysis:**
- Aggregate statistics can be misleading when underlying populations shift
- Simpson's Paradox applies: trends can reverse when data is improperly pooled
- Proper measurement requires compositional controls in labor market analysis
- Policy decisions based on headline statistics without compositional adjustment risk fundamental misdiagnosis

### Broader Implications

This analysis demonstrates a fundamental principle in empirical economics: **what you measure matters as much as how you measure it**. The choice between composition-adjusted and composition-naive measures can lead to opposite conclusions about economic conditions.

For policymakers, this has critical implications:
- Stimulus decisions based on misleading wage data could misallocate resources
- Labor market health assessments require compositionally-adjusted metrics
- Communication of economic statistics must clarify measurement methodology

---

## Technical Implementation

**Tools & Technologies:**
- **Python**: Core programming language for data pipeline
- **fredapi**: Federal Reserve API client for automated data ingestion
- **Pandas**: Time series manipulation, indexing, and transformation
- **Matplotlib**: Statistical visualization and comparative charting

**Reproducibility:**
- All data fetched programmatically via API (no manual downloads)
- Pipeline can be re-run with updated data to extend analysis
- Clear documentation of data transformations and calculations

---

## Economic Concepts Demonstrated

- **Money Illusion**: The tendency to think of value in nominal rather than real terms
- **Composition Effect / Simpson's Paradox**: How group-level statistics can mislead when subgroup composition changes
- **Real vs. Nominal Variables**: The critical distinction between dollars and purchasing power
- **Index Construction**: Understanding how different measurement approaches capture different phenomena

---

## Conclusion

This project bridges traditional economic theory with modern data science methods, demonstrating how automated data pipelines and rigorous statistical analysis can uncover hidden biases in standard economic indicators. The findings challenge conventional interpretations of pandemic-era labor market data and emphasize the necessity of composition-adjusted measures for accurate economic assessment.
