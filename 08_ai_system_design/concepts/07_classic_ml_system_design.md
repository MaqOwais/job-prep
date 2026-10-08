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
