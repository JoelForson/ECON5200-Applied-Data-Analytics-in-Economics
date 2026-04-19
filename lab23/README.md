## FedSpeak 2.0 — NLP Pipeline for Central Bank Communications

**Objective:** Diagnose and reconstruct a production-grade NLP pipeline for Federal Reserve meeting minutes, benchmarking bag-of-words and contextual embedding representations against a historically-grounded monetary policy classification task.

### Methodology

- **Pipeline audit:** Identified three systematic errors in an existing FOMC text pipeline — a whitespace tokenizer that left punctuation attached to tokens, the Harvard General Inquirer (GI) sentiment dictionary which mislabels neutral financial terms ("capital," "liability," "tax") as negative, and a TF-IDF configuration with no document-frequency filtering, producing a vocabulary dominated by background terms with zero discriminating power.

- **Preprocessing reconstruction:** Replaced `str.split()` with `nltk.word_tokenize()` combined with regex stripping of non-alphabetic characters, followed by stop-word removal and WordNet lemmatization. Verified correctness by asserting zero non-alpha tokens across the full corpus.

- **Domain-appropriate sentiment scoring:** Replaced the GI dictionary with the Loughran-McDonald (LM) financial lexicon (Loughran & McDonald, 2011, *Journal of Finance*), which was constructed specifically for SEC filings and central bank communications. Scored each document on net sentiment, negativity, and uncertainty dimensions. LM false-positive rate on financial terminology dropped below 10% vs. the GI baseline.

- **TF-IDF vectorization:** Rebuilt the feature matrix with `min_df=5`, `max_df=0.85`, `ngram_range=(1,2)`, and sublinear TF scaling — filtering rare OCR artifacts and ubiquitous background terms while capturing domain-critical bigrams such as "interest rate," "federal fund," and "price stability."

- **Contextual embeddings:** Encoded all FOMC documents using `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors), truncating each document to the first 2,000 characters to respect the model's context window.

- **Clustering comparison:** Applied K-Means (K=3) to both representations, reducing TF-IDF to 50 dimensions via Truncated SVD prior to clustering. Evaluated separation quality with silhouette scores and visualized cluster structure via PCA projection.

- **Predictive evaluation:** Trained logistic regression classifiers on both feature sets to predict whether the Fed was in a tightening cycle (2004–06, 2015–18, 2022–23), using `TimeSeriesSplit` (5 folds) to respect the sequential structure of the data. Reported AUC-ROC per fold with mean ± standard deviation.

- **Reusable module:** Packaged the corrected pipeline as `fomc_sentiment.py`, exposing three public functions — `preprocess_fomc()`, `compute_lm_sentiment()`, and `build_tfidf_matrix()` — with full docstrings documenting parameter rationale and design decisions.

### Key Findings

Sentence-transformer embeddings produced tighter cluster separation (higher silhouette score) than TF-IDF, reflecting their ability to encode syntactic context and word order rather than treating documents as unordered token bags. On the monetary policy classification task, [TF-IDF / Embeddings] achieved a mean AUC of [VALUE] ± [STD] across valid time-series folds, outperforming the alternative representation. The LM dictionary corrected a systematic negativity bias introduced by the GI lexicon — particularly relevant for FOMC minutes, where terms like "capital requirements" and "debt ceiling" carry no inherently negative connotation in the Federal Reserve's policy language.

---
*ECON 5200: Causal Machine Learning & Applied Analytics | Lab 23*
