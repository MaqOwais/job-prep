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
