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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why a cascade instead of running an LLM on every post?</b></summary>

**Cost and latency.** Most content is clearly fine or clearly bad. Cheap hash matching and small classifiers handle the bulk in milliseconds, and only uncertain items go to the expensive LLM or multimodal model, then to humans. This cuts cost by orders of magnitude.

</details>

<details>
<summary><b>Q2. How do you set thresholds per category?</b></summary>

By **harm severity and the cost of errors**: severe harms (child safety, self-harm) use low thresholds (high recall) and route to humans. Spam uses higher thresholds (high precision) to avoid annoying users. Tune on labeled data and adjust with appeal outcomes.

</details>

<details>
<summary><b>Q3. How do adversarial users evade moderation, and how do you respond?</b></summary>

Misspellings and leetspeak, text embedded in images, coded language, and slight image edits. Respond with **OCR** + multimodal models, perceptual hashing, normalization, frequent retraining on new examples, and red-teaming.

</details>

<details>
<summary><b>Q4. How do human reviewers fit in?</b></summary>

They handle uncertain and high-severity cases from **priority queues**, and their decisions become **training labels** (the data flywheel). Support them with well-being tooling (blurred previews, limited exposure) and track agreement between reviewers for quality.

</details>

<details>
<summary><b>Q5. Which metrics matter for moderation?</b></summary>

**Precision and recall per category**, the **prevalence** of harmful content actually seen by users, time to action, appeal overturn rate (false positives), and review queue latency.

</details>
