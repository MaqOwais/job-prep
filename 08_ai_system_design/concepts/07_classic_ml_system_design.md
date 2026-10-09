# 7. Classic ML System Design (non-LLM)

Many "ML system design" rounds are still about **recommendations, ranking, fraud, ads, search, and forecasting**. Your thesis work (VAEs, KDE, GANs, synthetic data) fits here.

📖 Chip Huyen, *Designing Machine Learning Systems* · [Hello Interview: ML system design](https://www.hellointerview.com/learn/ml-system-design/in-a-hurry/introduction)

## The ML design framework
1. **Business goal → ML objective.** "Increase watch time" → predict P(watch > 30 s) and rank by it.
2. **Data:** sources, labels (explicit or implicit), label delay, class imbalance, privacy.
3. **Features:** user, item, context, and cross features; embeddings; freshness requirements.
4. **Model:** baseline (heuristics or logistic regression) → gradient boosted trees (tabular) → deep models (two-tower, transformers). **Always start with a baseline.**
5. **Training:** train/validation/test split (**split by time** to avoid leakage), hyperparameter tuning, retraining cadence.
6. **Offline evaluation:** AUC, precision/recall, nDCG/MAP for ranking, RMSE for regression, calibration.
7. **Serving:** batch (precompute daily) vs online (real time) vs streaming features; latency budget.
8. **Online evaluation:** A/B tests on **business metrics**; guardrail metrics.
9. **Monitoring:** data drift, concept drift, feature skew between training and serving, model staleness → retraining triggers.

## Key components
| Component | Purpose | Examples |
|---|---|---|
| **Feature store** | One feature definition for training (offline) and serving (online), avoiding training/serving skew | Feast, SageMaker Feature Store, Tecton |
| Data pipeline | ETL, validation, labeling | Spark, Glue, Airflow, Great Expectations |
| Training pipeline | Reproducible training, experiment tracking | SageMaker Pipelines, Kubeflow, MLflow |
| Model registry | Versioning, approvals, lineage | MLflow, SageMaker Model Registry |
| Serving | Real-time endpoint or batch scoring | SageMaker endpoints, KServe, Triton |
| Monitoring | Drift, performance, data quality | SageMaker Model Monitor, Evidently |

## Common patterns
- **Two-stage recommendation:** candidate generation (cheap, recall-focused: two-tower embeddings + ANN search) → ranking (expensive, precision-focused: GBDT/deep model on hundreds of features) → re-ranking (diversity, business rules).
- **Cold start:** content-based features, popularity, exploration (bandits).
- **Imbalanced data (fraud):** resampling, class weights, precision-recall AUC instead of accuracy, and **synthetic data generation** (your thesis: VAEs/KDE/CTGAN!).
- **Feedback loops:** a model influences its own future training data. Add exploration and logging policies.
- **Online learning / frequent retraining** for fast-changing domains (ads, news).

## Interview tie-in to your research
> "For fraud with very few positive labels, I'd consider synthetic minority oversampling. In my thesis I generated synthetic tabular data with VAEs and adaptive KDE priors, and I validated fidelity with clustering agreement. I'd still validate on real held-out data, never on synthetic data alone."

## ✅ Self-check
- [ ] Walk through the 9 steps for "design YouTube recommendations"
- [ ] What is training/serving skew, and how does a feature store prevent it?
- [ ] Why split data by time?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why use a two-stage (candidate generation + ranking) recommender?</b></summary>

Scoring millions of items with a heavy model per request is too slow. **Candidate generation** cheaply narrows millions to ~1,000 with high recall (ANN on embeddings, heuristics). **Ranking** applies an expensive, accurate model to just those. Re-ranking then handles diversity and business rules.

</details>

<details>
<summary><b>Q2. What is training/serving skew, and how do you prevent it?</b></summary>

A model sees **differently computed features** in production than in training (different code paths, timing, or data), so offline metrics don't hold online. Prevent it with a **feature store** (one feature definition for both), logging the served features for training, and monitoring feature distributions.

</details>

<details>
<summary><b>Q3. Why split training data by time instead of randomly?</b></summary>

A random split **leaks future information** into training (e.g., later user behavior), inflating offline metrics. A time-based split (train on the past, validate on the future) mimics production, where the model always predicts the future.

</details>

<details>
<summary><b>Q4. How do you handle a heavily imbalanced dataset like fraud (0.1% positives)?</b></summary>

Use precision/recall, **PR-AUC**, and cost-weighted metrics rather than accuracy. Apply class weights or focal loss, resample (under/oversampling), generate **synthetic minority samples** (SMOTE, or VAE/CTGAN as in my thesis) while validating on real data only, and tune the decision threshold for the business cost tradeoff.

</details>

<details>
<summary><b>Q5. Offline metrics improved but the A/B test shows no gain. Why might that be?</b></summary>

Offline metrics don't match the **business metric**, training/serving skew, feedback loops or position bias in the logged data, novelty effects, too little statistical power, or the change affects too few users. Check the experiment setup, segment the results, and confirm the served features.

</details>
