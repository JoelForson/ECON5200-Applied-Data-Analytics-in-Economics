# Global Purchasing Power Parity Analysis via the Big Mac Index

## Objective

This analysis applies the concept of "Burgernomics" to empirically test the **Law of One Price** by examining currency valuation across international markets using McDonald's Big Mac as a standardized commodity benchmark.

---

## Methodology

- **Data Construction**: Manually structured a dataset using Python dictionaries based on The Economist's 2015 Big Mac Index, capturing local currency prices and official exchange rates across multiple countries
- **PPP Calculation**: Computed implied Purchasing Power Parity (PPP) exchange rates by comparing the domestic price of a Big Mac to the US benchmark price
- **Valuation Analysis**: Derived percentage currency misalignment by comparing implied PPP rates against actual market exchange rates, identifying overvalued and undervalued currencies
- **Technical Implementation**: Leveraged Python and Pandas for data manipulation, exchange rate calculations, and comparative analysis

---

## Key Findings

The analysis revealed significant deviations from purchasing power parity across global markets:

- **[Currency Name]** was found to be **overvalued by X%** relative to the US Dollar, suggesting the domestic Big Mac price exceeded what PPP theory would predict
- **[Currency Name]** exhibited **undervaluation of Y%**, indicating potential arbitrage opportunities or market inefficiencies
- Results demonstrate that the Law of One Price does not hold uniformly across international markets, likely due to factors such as non-tradable inputs (labor, rent), transportation costs, and local market conditions

---

## Economic Interpretation

The Big Mac Index serves as an accessible illustration of PPP theory, revealing how market exchange rates often diverge from their theoretical equilibrium. Persistent overvaluation may reflect higher productivity, stronger purchasing power, or elevated non-tradable costs, while undervaluation could indicate emerging market dynamics or currency market interventions.

---

## Tools & Technologies

- **Python**: Core programming language for analysis
- **Pandas**: Data structuring and computational analysis
