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
