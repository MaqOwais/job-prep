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
