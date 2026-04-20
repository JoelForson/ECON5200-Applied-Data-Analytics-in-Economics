# FedSpeak 2.0 — NLP Pipeline for Central Bank Communications

![Stack](https://img.shields.io/badge/stack-sklearn%20·%20nltk%20·%20sentence--transformers-blue)
![Domain](https://img.shields.io/badge/domain-Monetary%20Policy%20NLP-green)
![Module](https://img.shields.io/badge/module-fomc__sentiment.py-lightgrey)

## Objective

This project constructs and validates a production-grade NLP pipeline for quantifying hawkish/dovish sentiment in Federal Open Market Committee (FOMC) meeting minutes, diagnosing and correcting three systematic failures in a predecessor pipeline before benchmarking TF-IDF and sentence-embedding approaches against observed Fed rate decisions.

---

## Methodology

1. **Pipeline diagnostics & repair**
   Identified three critical defects: a whitespace-only tokenizer replaced with `nltk.word_tokenize`; the Harvard General Inquirer sentiment lexicon replaced with the domain-appropriate Loughran-McDonald financial dictionary; and misconfigured TF-IDF `min_df`/`max_df` thresholds corrected for sparse financial corpora.

2. **Sentiment scoring with Loughran-McDonald**
   Computed document-level net sentiment scores using the LM financial lexicon — purpose-built for regulatory and central bank language — capturing directional tone missed by general-purpose dictionaries.

3. **Dual-representation feature engineering**
   Encoded FOMC documents under two paradigms: sparse TF-IDF vectors (50-dim SVD reduction) and dense semantic embeddings via `all-MiniLM-L6-v2` (sentence-transformers), enabling direct comparison of lexical versus contextual representations.

4. **Clustering & predictive benchmarking**
   Applied K-Means clustering under both representations and evaluated predictive power against realized Fed rate decisions using 5-fold time-series cross-validation with AUC-ROC as the primary discrimination metric.

5. **Reusable module packaging**
   Encapsulated validated logic in `fomc_sentiment.py` exposing three public functions: `preprocess_fomc()`, `compute_lm_sentiment()`, and `build_tfidf_matrix()`.

---

## Key Findings

### Primary result — TF-IDF wins

TF-IDF (50-dim SVD) achieved a mean AUC of **0.797 ± 0.227** across valid time-series folds, outperforming sentence-transformer embeddings (AUC 0.714 ± 0.213) for predicting Federal Reserve tightening decisions — a non-trivial result suggesting that term-frequency patterns in FOMC language carry more discriminative signal than contextual semantics for this classification task.

### Lexicon sensitivity

Switching from Harvard GI to Loughran-McDonald produced substantially different document-level sentiment scores, confirming that domain-matched lexicons are a methodological requirement — not a stylistic preference — for central bank text analysis.

### High variance caveat

Both approaches exhibited high fold-level variance (±0.22–0.23 AUC), with early folds skipped due to single-class splits — consistent with the severe class imbalance in the dataset (72 tightening vs. 168 easing/hold meetings). Mean AUC figures should be interpreted as directional rather than definitive.

### Representation tradeoffs

TF-IDF and sentence-embedding clustering produced meaningfully distinct groupings of FOMC minutes — suggesting that lexical frequency and contextual semantics capture complementary dimensions of monetary policy communication that may warrant ensemble treatment in applied research.

---

## AUC-ROC Summary

| Representation | Mean AUC | Std Dev | Valid Folds |
|---|---|---|---|
| TF-IDF (50-dim SVD) | 0.797 | ±0.227 | 3 of 5 |
| Sentence-transformer embeddings | 0.714 | ±0.213 | 3 of 5 |

> **Note:** Folds 1 and 2 were skipped for both models due to single-class splits, a consequence of the chronological ordering of FOMC tightening cycles in the dataset.

---

## Module Reference

**`fomc_sentiment.py`**

| Function | Description |
|---|---|
| `preprocess_fomc(text)` | Tokenizes and cleans FOMC document text using `nltk.word_tokenize` |
| `compute_lm_sentiment(tokens)` | Scores net sentiment using the Loughran-McDonald financial lexicon |
| `build_tfidf_matrix(corpus)` | Constructs a TF-IDF matrix with corrected `min_df`/`max_df` parameters |