# 4. LLM Serving & Inference

📖 Deeper: [vLLM docs](https://docs.vllm.ai/) · [PagedAttention paper](https://arxiv.org/abs/2309.06180) · [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference)

## Why LLM serving is different
- Requests have **wildly different lengths** (10 tokens vs 100K).
- Generation is **sequential** (one token at a time) and **memory-bandwidth bound**.
- GPUs are **expensive and scarce**, so utilization is everything.
- Users expect **streaming** output.

## Key optimizations (know what each one does)
| Technique | What it does | Gain |
|---|---|---|
| **Continuous (in-flight) batching** | Add and remove requests from the GPU batch at every decode step instead of waiting for the whole batch | Large throughput gain |
| **PagedAttention (vLLM)** | Manages the KV cache in pages, like OS virtual memory → little fragmentation, more concurrent requests | 2–4× throughput |
| **Prefix / prompt caching** | Reuse the KV cache for shared prompt prefixes (system prompt, documents) | Lower TTFT and cost |
| **Quantization** (FP8/INT8/INT4, AWQ/GPTQ) | Smaller weights → fewer GPUs, faster decode | Some quality loss; evaluate it |
| **Speculative decoding** | A small draft model proposes tokens; the big model verifies several at once | 2–3× faster decode, same output |
| **Tensor / pipeline parallelism** | Split a big model across GPUs | Needed for 70B+ models |
| **Disaggregated prefill/decode** | Separate GPU pools for prefill (compute) and decode (memory) | Better utilization at scale |
| **FlashAttention** | Memory-efficient attention kernel | Faster, longer contexts |
| **LoRA multiplexing** | One base model in memory + many small adapters swapped per request | Serve many fine-tunes cheaply |

**Serving engines:** vLLM, TensorRT-LLM, TGI, SGLang. Managed options: Bedrock, SageMaker endpoints, and other cloud providers.

## Metrics
- **TTFT** (time to first token): user-perceived responsiveness, driven by prefill and queueing.
- **TPOT / ITL** (time per output token): streaming smoothness.
- **Throughput** (tokens/s per GPU) and **goodput** (throughput while still meeting SLOs).
- GPU utilization, KV cache utilization, queue depth, $ per 1M tokens.

## Scaling and reliability
- **Autoscale on queue depth or KV-cache utilization**, not on CPU. GPU cold starts (loading weights) take minutes, so keep a warm pool and use predictive scaling.
- **Routing:** send requests with the same prefix to the same replica (cache affinity). Use **least-outstanding-tokens** load balancing, not round robin.
- **Priority queues:** interactive vs batch traffic. Shed or queue batch jobs under load.
- **Fallbacks:** another region, another model size, or another provider.
- **Batch inference** for offline jobs: 50%+ cheaper, run off-peak.
- Capacity planning: reserved or provisioned throughput for the base load, on-demand for spikes.

## API vs self-hosting
| Managed API (Bedrock, etc.) | Self-host open weights |
|---|---|
| No GPU ops, the latest frontier models, pay per token | Full control, data stays in your VPC, cheaper at **high steady volume** |
| Less control, rate limits, vendor dependency | GPU ops burden, capacity risk, you own reliability |
> Rule of thumb: **start with an API**. Self-host when volume is high and steady, when you need customization, or for strict data residency.

## ✅ Self-check
- [ ] Explain continuous batching and PagedAttention in 30 seconds each
- [ ] What limits concurrency on a GPU? (The KV cache.)
- [ ] What would you autoscale on, and why not CPU?
- [ ] When would you self-host instead of using an API?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What is continuous batching?</b></summary>

Instead of waiting for a whole batch to finish, the server **adds new requests and removes finished ones at every decode step**. The GPU stays full even though requests have very different lengths, which multiplies throughput compared to static batching.

</details>

<details>
<summary><b>Q2. What problem does PagedAttention (vLLM) solve?</b></summary>

**KV cache memory fragmentation.** Reserving contiguous memory for each request's maximum length wastes most of the GPU memory. PagedAttention stores the KV cache in **fixed-size pages** (like OS virtual memory), allocated on demand and shareable between requests with a common prefix. More concurrent requests fit, giving much higher throughput.

</details>

<details>
<summary><b>Q3. Why not autoscale LLM servers on CPU utilization?</b></summary>

CPU usage barely reflects GPU load. Scale on **queue depth / pending requests**, **KV-cache utilization**, GPU utilization, and **TTFT** against the SLO. GPU instances also take minutes to load model weights, so keep warm capacity and scale predictively.

</details>

<details>
<summary><b>Q4. How does speculative decoding speed up generation without changing the output?</b></summary>

A small, fast **draft model** proposes several tokens. The big model **verifies them in one forward pass** and accepts the longest correct prefix (rejection sampling keeps the output distribution identical). When most drafts are accepted, you get 2–3× faster decoding.

</details>

<details>
<summary><b>Q5. When should a company self-host open-weight models instead of using an API?</b></summary>

When volume is **high and steady** (GPU cost per token beats API pricing), data must stay inside its own network for compliance, it needs deep customization (fine-tunes, custom decoding), or it wants to avoid vendor limits. Otherwise an API is cheaper in engineering time and gives the latest models.

</details>
