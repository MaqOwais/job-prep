# 🟢 03. Content Moderation Service (text and images)

📖 Concepts: [Safety](../../concepts/06_safety_security.md) · [Classic ML](../../concepts/07_classic_ml_system_design.md)
⏱️ Try it yourself first: 30 minutes.

## 1. Requirements
**Functional:** classify user posts (text + images) as allowed / needs review / blocked across policy categories (hate, violence, sexual content, spam, self-harm); appeals; human review queue.
**Non-functional:** 5K posts/s at peak, < 200 ms for synchronous checks, **high recall on severe harms**, low false positives on normal content, explainable decisions for appeals.

## 2. Key idea: a cascade (cheap → expensive)
```
Post → [1] hash match (known bad images/text: perceptual hashing) → block instantly
     → [2] fast classifiers (small fine-tuned models, ms latency, cheap) → score per category
          high confidence bad  → block
          high confidence safe → allow   (the vast majority)
          uncertain            → [3] LLM / multimodal model with the written policy in the prompt (slower, costly)
                                      → still uncertain or severe → [4] human review queue (priority by severity)
Decisions + reviewer labels → training data → retrain classifiers (data flywheel)
```
**Why a cascade?** Running an LLM on 5K posts/s is expensive. Most content is clearly fine, so the cheap layers handle it.

## 3. Deep dives
- **Thresholds per category:** severe harms (child safety, self-harm) get low thresholds (high recall) and route to humans. Spam gets higher thresholds.
- **Sync vs async:** a quick check before publishing, then deeper async re-scans (e.g., after a policy update or when a post goes viral).
- **Human review tooling:** priority queues, blurred previews, reviewer well-being, inter-rater agreement metrics.
- **Adversarial users:** misspellings, text inside images (OCR), coded language. Retrain often and red-team.
- **Metrics:** precision/recall per category, prevalence of harmful content seen by users, appeal overturn rate, review queue latency.
- **Explainability:** store the category, the model version, and the policy clause for each decision, for appeals and audits.

## ✅ Takeaways
**Classifier cascade** with confidence thresholds, LLMs only for ambiguous cases, a human-in-the-loop queue, and a labeling flywheel.
