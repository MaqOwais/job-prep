# 1. LLM Fundamentals (what you need for design rounds)

You don't need to derive attention. You do need to reason about **tokens, memory, latency, and cost**.

## Core vocabulary
| Term | One-liner |
|---|---|
| **Token** | A sub-word unit. Roughly **1 token ≈ 0.75 English words ≈ 4 characters**. |
| **Context window** | Maximum input + output tokens per request (e.g., 128K–1M+ for frontier models) |
| **Transformer** | Stacked self-attention + feed-forward layers. Attention cost grows **quadratically** with sequence length (with mitigations). |
| **Prefill** | Processing the whole prompt in parallel. It's **compute-bound** and determines **time to first token (TTFT)**. |
| **Decode** | Generating one token at a time. It's **memory-bandwidth-bound** and determines **tokens/second**. |
| **KV cache** | Stored attention keys and values for past tokens, so they aren't recomputed. Uses a lot of GPU memory. |
| **Embedding** | A dense vector representing meaning, used for search, clustering, and RAG |
| **Temperature / top-p** | Sampling randomness. Use 0 for deterministic extraction, higher for creative writing. |
| **Structured output** | JSON mode / constrained decoding / tool schemas, for reliable parsing |
| **Fine-tuning** | Full fine-tuning, or **PEFT/LoRA** (train small adapter matrices: cheap, swappable per tenant) |
| **RLHF / DPO** | Aligning a model to preferences after pretraining |
| **Quantization** | Lower-precision weights (FP16 → INT8/INT4/FP8): less memory, faster, slight quality loss |
| **MoE** | Mixture of experts: only some parameters are active per token, giving cheaper inference for the model size |

## Back-of-envelope math (practice this)
**GPU memory for weights:** params × bytes per param.
- 7B model at FP16 (2 bytes) ≈ **14 GB**. At INT4 ≈ 3.5–4 GB.
- 70B at FP16 ≈ **140 GB**, so it needs multiple GPUs (an 80 GB H100 × 2+) or quantization.

**KV cache per token** ≈ 2 (K and V) × layers × hidden size × bytes. For a 7B-class model that's roughly **0.5 MB per token** at FP16 (less with grouped-query attention). So 4K context × 32 concurrent requests ≈ tens of GB. **The KV cache, not the weights, often limits concurrency.**

**API cost estimate:**
```
requests/day × (input_tokens × $in + output_tokens × $out) / 1M
e.g. 1M req/day × (2,000 in × $3/M + 300 out × $15/M) ≈ $6,000 + $4,500 = $10.5K/day
```
→ This is why **prompt caching, smaller models for easy tasks, and shorter contexts** matter.

**Latency:** total ≈ TTFT + (output tokens ÷ tokens per second). E.g. 0.5 s + 300 / 60 tok/s ≈ **5.5 s**, so **stream** the output.

## Choosing an approach (classic interview question)
| Approach | Use when | Cost / effort |
|---|---|---|
| **Prompt engineering** (few-shot, system prompts) | Always start here | Lowest |
| **RAG** | Needs private, fresh, or citable knowledge | Medium |
| **Fine-tuning (LoRA)** | Consistent style or format, domain jargon, a smaller cheaper model for a narrow task, or distillation | Medium-high, needs data |
| **Pretraining** | Almost never (a new language or domain at massive scale) | Huge |

> "Fine-tuning teaches **behavior and format**. RAG supplies **knowledge**. Most products need RAG first."

## Model selection tradeoffs
Quality vs latency vs cost vs context length vs data privacy vs licensing (open weights vs API). **Route** easy requests to small, fast models and hard ones to frontier models.

## ✅ Self-check
- [ ] Estimate GPU memory for a 13B model at FP16 and at INT4
- [ ] Explain prefill vs decode and which one drives TTFT
- [ ] Estimate monthly API cost for a given traffic level
- [ ] RAG vs fine-tuning: give one example where each is right
