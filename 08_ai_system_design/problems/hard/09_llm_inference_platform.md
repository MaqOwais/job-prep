# 🔴 09. LLM Inference Platform (serve many models to many customers, like a model-API provider)

📖 Concepts: [LLM serving & inference](../../concepts/04_llm_serving_inference.md) · [LLM fundamentals: memory math](../../concepts/01_llm_fundamentals.md)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** OpenAI-style API serving dozens of models (7B–400B+), streaming, many tenants, per-tenant rate limits and priority tiers, batch API, fine-tuned (LoRA) variants.
**Non-functional:** TTFT p95 < 1 s for interactive traffic, high GPU utilization (GPUs are the main cost), multi-region availability, fair sharing between tenants.

## 2. Estimates (example)
Assume **10K req/s** at peak, 1K input + 300 output tokens → 3M output tokens/s. If one GPU replica produces ~2–5K tokens/s with good batching → **roughly 600–1,500 GPUs** for decode. **GPU count and cost are the headline numbers.**

## 3. High-level design
```
Clients → Global LB / GeoDNS → API frontends (auth, quotas, token-bucket limits, request validation)
   → Request router (per region):
        picks model pool → replica by: KV-cache/prefix affinity, least outstanding tokens, health
        priority queues per tier (interactive > standard > batch), admission control / load shedding
   → Model pools: replicas running vLLM/TensorRT-LLM
        small models: 1 GPU/replica; large: tensor-parallel across 4–8 GPUs (one node); huge: + pipeline parallel
        LoRA adapters hot-swapped on shared base models
   → stream tokens back through the frontends
Control plane: model registry + weights in object storage (pre-staged to local NVMe), autoscaler, capacity planner
Batch API: queue → fill idle GPU capacity off-peak (cheaper price)
Metering: token counts → Kafka → billing; observability: TTFT, TPOT, queue time, KV utilization per pool
```

## 4. Deep dives
- **Batching and memory:** continuous batching + PagedAttention; the KV cache limits concurrency; prefix caching for shared system prompts.
- **Prefill/decode disaggregation:** separate GPU pools, so long prompts don't stall token streaming for others.
- **Autoscaling:** signals are queue depth, KV utilization, and TTFT. Weight loading takes minutes, so keep warm spare capacity, pre-stage weights, and scale predictively from traffic patterns.
- **Multi-model packing:** popular models get dedicated pools; long-tail models share GPUs or scale to zero, with a cold-start tradeoff.
- **Fairness and isolation:** per-tenant token limits, weighted fair queuing, priority tiers, provisioned throughput contracts for big customers.
- **Reliability:** health checks that detect GPU errors (Xid errors, NaN outputs), drain and replace, cross-region failover, graceful degradation (fall back to a smaller model when enabled).
- **Cost levers:** quantization (FP8), speculative decoding, high utilization through batch backfill, cheaper accelerators (Inferentia/TPU) for some models.
- **Safety:** abuse detection, content filters, per-tenant isolation of logs and caches.

## ✅ Takeaways
Frontends + **smart router (prefix affinity, least tokens, priorities)** + GPU model pools (TP/PP, LoRA) + KV-aware autoscaling + batch backfill + metering. Lead with GPU math.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Estimate the GPUs needed for 10K requests/s with 300 output tokens each.</b></summary>

10K × 300 = **3M output tokens/s**. If one replica sustains ~2–5K tokens/s with continuous batching, you need roughly **600–1,500 replicas** (× GPUs per replica for large models), plus headroom and redundancy. State your assumptions about model size and throughput.

</details>

<details>
<summary><b>Q2. How should the router pick a replica?</b></summary>

Prefer replicas that already hold the **prompt prefix in their KV cache** (cache affinity), then **least outstanding tokens** (not request count), and respect health and priority tiers. Round robin ignores very different request costs.

</details>

<details>
<summary><b>Q3. How do you give fair service to many tenants?</b></summary>

Per-tenant **token rate limits** and quotas, **priority tiers** (interactive > standard > batch), weighted fair queuing, admission control and load shedding under overload, and **provisioned throughput** for customers who pay for guaranteed capacity.

</details>

<details>
<summary><b>Q4. Why separate prefill and decode onto different GPUs?</b></summary>

Prefill is **compute-bound** and bursty (long prompts), decode is **memory-bandwidth-bound** and steady. On the same GPU, long prefills stall the token streams of other requests. Disaggregating lets each pool use the right hardware and batching strategy, improving both TTFT and tokens/s.

</details>

<details>
<summary><b>Q5. How do you serve hundreds of fine-tuned variants cheaply?</b></summary>

Use **LoRA adapters** on a shared base model: keep the base weights loaded once, hot-swap or batch multiple small adapters per request (multi-LoRA serving), and only dedicate GPUs to full fine-tunes that justify it.

</details>
