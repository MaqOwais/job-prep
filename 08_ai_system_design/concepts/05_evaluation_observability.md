# 5. Evaluation & Observability

> "How would you know it's working?" is the question that separates strong candidates in AI design rounds. **Always include an evaluation section.**

## The evaluation stack
| Layer | What | When |
|---|---|---|
| **Offline eval set** ("golden set") | 100–1,000+ representative inputs with expected outputs or rubrics, including edge cases and adversarial inputs | Every prompt, model, or retrieval change (CI for prompts) |
| **Automated metrics** | Exact match, F1, BLEU/ROUGE (weak for LLMs), code tests pass@k, JSON schema validity | Cheap and fast |
| **LLM-as-judge** | A strong model grades outputs against a rubric (pairwise comparisons are more reliable) | Scales human judgment; calibrate it against humans and watch for bias |
| **Human evaluation** | Expert raters, side-by-side comparisons | Ground truth, expensive |
| **Online metrics** | Thumbs up/down, regenerations, edits, task completion, deflection rate, retention, conversion | Production |
| **A/B tests** | Compare prompts or models on live traffic | Before full rollout |

## RAG-specific metrics (evaluate retrieval and generation separately)
| Component | Metric |
|---|---|
| Retrieval | **Recall@k** (is the right chunk in the top k?), precision@k, MRR, nDCG |
| Generation | **Faithfulness / groundedness** (is every claim supported by the context?), answer relevance, citation accuracy |
| End to end | Correctness vs a reference, helpfulness, refusal appropriateness |
Tools: RAGAS, DeepEval, TruLens, promptfoo, Bedrock model evaluation.

## Agent evaluation
Task success rate, number of steps and tokens per task, tool-call accuracy, cost per task, safety violations. Replay recorded traces for regression tests.

## Observability (LLMOps)
- **Trace every request:** prompt version, model, retrieved chunks, tool calls, latency per step, tokens, cost, user feedback.
- Tools: LangSmith, Langfuse, Arize Phoenix, OpenTelemetry GenAI conventions, CloudWatch / X-Ray.
- **Dashboards:** TTFT and p95 latency, error rate, $ per request, cache hit rate, guardrail trigger rate, thumbs-down rate.
- **Drift:** input topic drift, embedding distribution shift, quality decay after provider model updates. **Pin model versions.**
- **Prompt management:** version prompts like code, review changes, roll back.

## The data flywheel
Production traces → sample failures (thumbs down, low judge scores) → label them → add them to the eval set → improve prompts, retrieval, or fine-tune → redeploy. **This is how AI products get better over time.** Mention it.

## ✅ Self-check
- [ ] Design an evaluation plan for a RAG chatbot (offline + online)
- [ ] Recall@k vs faithfulness: what does each catch?
- [ ] Pitfalls of LLM-as-judge (position bias, verbosity bias, self-preference) and how to mitigate them

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How would you evaluate a RAG chatbot before launch?</b></summary>

Build a **golden set** of real questions with reference answers and source documents. Measure **retrieval** (recall@k, MRR) and **generation** (faithfulness / groundedness, answer relevance, citation accuracy) with automated metrics plus an **LLM judge** calibrated against human ratings. Gate releases on these scores.

</details>

<details>
<summary><b>Q2. What are the pitfalls of LLM-as-judge, and how do you mitigate them?</b></summary>

**Position bias** (prefers the first answer), **verbosity bias**, **self-preference** (favors its own model family), and inconsistency. Mitigate: swap positions and average, use explicit rubrics, use pairwise comparisons, use a different judge model, and validate agreement against human labels.

</details>

<details>
<summary><b>Q3. Which online metrics show whether an AI feature is working?</b></summary>

Task completion and success rate, **thumbs up/down**, regeneration and edit rate, escalation or deflection rate (support bots), retention and repeat usage, latency (TTFT), and **cost per request**, plus guardrail trigger rates.

</details>

<details>
<summary><b>Q4. What should you log for every LLM request?</b></summary>

Prompt and template version, model and parameters, retrieved chunk IDs, tool calls and results, token counts, latency per step, cost, the user's feedback, and guardrail decisions. Redact PII, and link everything with a trace ID.

</details>

<details>
<summary><b>Q5. What is the data flywheel?</b></summary>

Production traces → find failures (thumbs down, low judge scores) → label them → add them to the **eval set** and training data → improve prompts, retrieval, or fine-tunes → redeploy → repeat. Each iteration makes the product measurably better.

</details>
