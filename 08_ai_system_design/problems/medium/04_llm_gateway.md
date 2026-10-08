# 🟡 04. LLM Gateway (a central proxy for all LLM calls in a company)

📖 Concepts: [Serving](../../concepts/04_llm_serving_inference.md) · Related: [Rate limiter](../../../02_high_level_design/12_problems/easy/02_rate_limiter.md) · [Caching](../../../02_high_level_design/06_caching/)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** one API for many model providers (Bedrock, OpenAI, Anthropic, self-hosted); per-team API keys and **token-based** rate limits and budgets; fallback when a provider fails; response caching; logging and cost attribution; PII redaction.
**Non-functional:** adds < 20 ms latency, supports streaming, highly available (it's on every request path).

## 2. High-level design
```
Internal apps → Gateway (stateless, autoscaled, multi-AZ)
   1. authN (team key) → policy lookup (allowed models, budgets, data rules) [cached]
   2. token-bucket rate limit on tokens/min AND requests/min (Redis)
   3. input guardrails: PII redaction, size limits
   4. cache lookup: exact-match hash → semantic cache (embedding similarity ≥ threshold)
   5. router: pick model/provider (by policy, cost, latency, health) → provider adapter (unified schema)
   6. stream response back; on error/timeout → retry another region/provider (circuit breaker per provider)
   7. async: usage event (tokens in/out, $, latency, team) → Kafka → billing/analytics; trace store
```

## 3. Deep dives
- **Token-aware rate limiting:** you don't know the output length up front. Reserve `max_tokens`, then reconcile with the actual usage after the response.
- **Routing strategies:** a fixed model per use case; cost-based (cheapest model that passes evals); **complexity-based** (a small classifier sends easy prompts to a small model); latency-based; or failover only.
- **Semantic cache:** works well for FAQ-style traffic. Risks: returning a wrong answer for a subtly different question, and leaking data across users. Scope caches per tenant and set a conservative similarity threshold.
- **Circuit breakers + health checks** per provider and region; respect providers' 429 responses with backoff.
- **Streaming proxy:** keep SSE connections efficient (async I/O); count tokens as they stream.
- **Cost attribution:** per team, app, and feature tags → dashboards and budget alerts → hard stop at the limit.
- **Compliance:** route sensitive data only to approved providers or regions; keep audit logs (redacted).

## ✅ Takeaways
Unified API + **token-based** limits and budgets + routing and fallbacks + exact and semantic caching + cost attribution. It's the classic API gateway pattern adapted for LLMs.
