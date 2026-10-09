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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why build a central LLM gateway at all?</b></summary>

One place for **auth, token-based rate limits and budgets, provider routing and fallbacks, caching, PII redaction, logging, and cost attribution**. Without it, every team re-implements these and the company has no visibility into usage or spend.

</details>

<details>
<summary><b>Q2. How do you rate limit by tokens when the output length is unknown?</b></summary>

**Reserve** max_tokens (or an estimate) from the token bucket at request time, then **reconcile** with the actual usage after the response finishes and refund the difference. Combine it with a requests-per-minute limit.

</details>

<details>
<summary><b>Q3. What are the risks of semantic caching, and how do you control them?</b></summary>

It can return an answer to a **subtly different question** (wrong answer) or **leak data between users**. Control it with a conservative similarity threshold, per-tenant or per-user cache scopes, excluding personalized or time-sensitive prompts, and short TTLs.

</details>

<details>
<summary><b>Q4. How does failover between providers work?</b></summary>

Health checks and a **circuit breaker** per provider and region. On errors, timeouts, or 429s, retry with backoff on an **equivalent model** from another region or provider. Normalize request and response formats through adapters so callers don't notice. Respect data rules (some data may only go to approved providers).

</details>

<details>
<summary><b>Q5. How do you attribute costs to teams?</b></summary>

Every request carries the team, app, and feature in its key or headers. The gateway records input/output tokens × model price as a **usage event** (to Kafka → a warehouse), drives dashboards and budget alerts, and enforces hard caps.

</details>
