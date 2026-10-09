# 🟡 07. Recommendation System (YouTube / Netflix / Amazon "recommended for you")

📖 Concepts: [Classic ML system design](../../concepts/07_classic_ml_system_design.md) · [Deep Neural Networks for YouTube Recommendations (paper)](https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** a personalized home feed of items (videos or products); updates with recent behavior; handles new users and new items.
**Non-functional:** 100M users, 10M items, < 200 ms to build a feed. **Business metric:** watch time or purchases, not just clicks.

## 2. ML framing
Predict **P(engagement | user, item, context)**, e.g. P(watch > 30 s) or P(purchase). Rank by expected value. Labels come from implicit feedback (clicks, watch time) and explicit feedback (ratings, likes).

## 3. Multi-stage architecture
```
Request (user_id, context) →
 [1] CANDIDATE GENERATION (10M → ~1,000), cheap and recall-oriented, several sources merged:
        two-tower model: user embedding · item embeddings → ANN search
        collaborative filtering, "because you watched X", trending, followed creators
 [2] RANKING (1,000 → 100): heavier model (GBDT or deep cross network) with hundreds of features
        user features, item features, user×item cross features, context (time, device)
 [3] RE-RANKING (100 → 20): diversity, freshness, remove already seen, business rules, fairness
 → feed
OFFLINE: event logs → feature pipelines → feature store (offline + online) → daily/hourly training → model registry
ONLINE: real-time features (last N items viewed) via streaming (Kafka/Flink) → online feature store (Redis/DynamoDB)
```

## 4. Deep dives
- **Two-tower model:** user tower and item tower trained so their dot product predicts engagement. Item embeddings are precomputed and indexed for ANN search; the user embedding is computed at request time.
- **Cold start:** new users get popularity + onboarding questions + contextual signals. New items get content-based embeddings (text, image) + exploration traffic (bandits).
- **Feedback loops / popularity bias:** add exploration and log propensities for unbiased evaluation.
- **Training/serving skew:** a feature store with the same feature code for training and serving.
- **Evaluation:** offline recall@k (candidate generation), AUC / nDCG (ranking); online **A/B tests on watch time and retention**, with guardrail metrics (diversity, complaints).
- **Scaling:** precompute candidates for inactive users in batch; real-time path for active users.

## ✅ Takeaways
**Candidate generation → ranking → re-ranking**, two-tower + ANN, a feature store, cold-start strategies, and A/B tests on business metrics.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Explain the two-tower model and how it's served.</b></summary>

A **user tower** and an **item tower** each output an embedding, trained so their dot product predicts engagement. Item embeddings are **precomputed and indexed for ANN search**. At request time the user embedding is computed and the nearest items are retrieved as candidates.

</details>

<details>
<summary><b>Q2. How do you handle new users and new items (cold start)?</b></summary>

**New users:** popularity, onboarding questions, context (location, device, time), then quick adaptation from their first interactions. **New items:** content-based embeddings (text and image features) and **exploration** traffic (bandits) to gather engagement data.

</details>

<details>
<summary><b>Q3. Why optimize for watch time or purchases rather than clicks?</b></summary>

Clicks are easy to game (clickbait) and don't capture real value. Optimizing for **downstream satisfaction** (watch time, completion, purchases, retention) aligns the model with user and business value. Usually several objectives are combined into one ranking score.

</details>

<details>
<summary><b>Q4. How do you stop the model from only recommending already popular items?</b></summary>

Add **exploration** (ε-greedy or bandits), diversity re-ranking, popularity debiasing, inverse-propensity weighting in training, and fairness or creator-exposure constraints. Without them, a feedback loop keeps amplifying popularity.

</details>

<details>
<summary><b>Q5. How do real-time signals get into recommendations?</b></summary>

Stream user events (Kafka → Flink) into an **online feature store** (Redis/DynamoDB) with features like "last 10 items viewed". The ranking model reads them at request time, so recommendations react within seconds of a click.

</details>
