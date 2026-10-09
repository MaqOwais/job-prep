# 🟡 06. AI Coding Assistant (GitHub Copilot / Amazon Q Developer style inline completion)

📖 Concepts: [Serving](../../concepts/04_llm_serving_inference.md) · [RAG](../../concepts/02_rag_retrieval.md) · [Evaluation](../../concepts/05_evaluation_observability.md)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** suggest code inline as the developer types (ghost text); multi-line completions; aware of the open files and the repository; chat about the code (stretch goal).
**Non-functional:** **very low latency** (< 300–500 ms or it feels laggy), huge request volume (a request on almost every pause in typing), code privacy (enterprise), cost control.

## 2. Estimates
1M developers × ~1,000 completion requests/day ≈ 1B requests/day ≈ **12K QPS**, with short outputs (~20–50 tokens) but large prompts (~2K tokens of context). **Prefill cost and latency dominate.**

## 3. High-level design
```
IDE plugin:
  debounce (~75–150 ms) → cancel in-flight requests when the user keeps typing
  build context: prefix + suffix around the cursor (Fill-in-the-Middle), open tabs, imports,
                 similar snippets from the repo (local index), language/file path
  local cache of recent completions
     ↓ HTTPS/HTTP2 to the nearest region
Completion service → prompt assembly + token budget → small, fast code model (self-hosted, GPU)
     → post-process: stop at a block boundary, dedupe, syntax check, filter secrets/licensed code matches
     ← stream back; IDE shows the ghost text
Telemetry: shown / accepted / edited-after-accept → metrics + training data (opt-in)
```

## 4. Deep dives
- **Fill-in-the-middle (FIM):** the model sees the code before *and after* the cursor, giving much better completions.
- **Context selection** is the key quality lever: rank candidate snippets (open tabs, recently edited files, embedding-similar code) to fit the token budget.
- **Latency tricks:** a small specialized model, speculative decoding, prefix caching (consecutive requests share most of the prompt), regional GPU clusters, HTTP/2 connection reuse, request cancellation.
- **Two tiers:** fast small model for inline completion, larger model for chat and "explain/refactor" requests.
- **Privacy:** enterprise mode with no retention or training on customer code, a VPC or on-prem option, a secret-detection filter.
- **Metrics:** **acceptance rate**, characters retained after 30 s, latency p50/p95, and productivity studies. Offline: pass@k on HumanEval-style tests and repo-level benchmarks.

## ✅ Takeaways
Latency-first design: debounce + cancel + FIM + smart context packing + a small fast model + prefix caching. Measure acceptance rate.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why is latency so critical for inline code completion, and how do you achieve it?</b></summary>

Suggestions must appear **while the developer pauses** (roughly < 300–500 ms) or they get in the way. Use client debounce and request cancellation, a **small specialized model**, prefix caching (consecutive prompts share most tokens), regional GPUs, HTTP/2 connection reuse, and short outputs.

</details>

<details>
<summary><b>Q2. What is fill-in-the-middle (FIM)?</b></summary>

The model is trained to generate the code between a **prefix** (code before the cursor) and a **suffix** (code after it), so completions fit the surrounding code (closing brackets, matching the function that follows) instead of only continuing from the left.

</details>

<details>
<summary><b>Q3. How do you choose which context goes into the prompt?</b></summary>

Rank candidate snippets by relevance and fit them into a token budget: the code around the cursor, open tabs and recently edited files, imports and definitions of symbols used nearby, and embedding-similar code from the repo. Context selection is often the biggest quality lever.

</details>

<details>
<summary><b>Q4. How do you measure whether the assistant helps?</b></summary>

**Acceptance rate**, **retention** (accepted code still present after N seconds or minutes), latency percentiles, the share of code written with assistance, and controlled productivity studies. Offline: pass@k on test-based benchmarks.

</details>

<details>
<summary><b>Q5. What privacy concerns do enterprises have, and how do you address them?</b></summary>

Proprietary code leaving the company or being used for training. Offer **zero data retention**, no training on customer code, encryption, regional or VPC deployment options, secret-detection filters on prompts and outputs, and admin controls and audit logs.

</details>
