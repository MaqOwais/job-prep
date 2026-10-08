# 🔴 10. Fine-Tuning Platform (customers fine-tune models on their own data)

📖 Concepts: [LLM fundamentals](../../concepts/01_llm_fundamentals.md) · [Evaluation](../../concepts/05_evaluation_observability.md) · [Classic ML pipelines](../../concepts/07_classic_ml_system_design.md)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** customers upload a training dataset (JSONL prompt/response pairs), pick a base model and hyperparameters, start a job, watch progress and metrics, evaluate the result, and deploy it to an endpoint. Supports LoRA and full fine-tuning.
**Non-functional:** multi-tenant with **strict data isolation**, efficient use of a shared GPU fleet, fault tolerance for long jobs, reproducibility.

## 2. High-level design
```
Customer → API (create dataset, create job, get status) → Job DB (state machine: QUEUED→VALIDATING→TRAINING→EVALUATING→SUCCEEDED/FAILED)
Dataset upload → S3 (per-tenant prefix, KMS key per tenant)
   → Validation workers: schema, token counts, PII/toxicity scan, dedupe, train/validation split, cost estimate
Scheduler: GPU-aware job queue (priority, quotas per tenant, gang scheduling for multi-GPU jobs, preemption for low tier)
   → Training cluster (Kubernetes/Slurm or SageMaker HyperPod):
        load base weights (cached on nodes) → LoRA/QLoRA or full FT (FSDP/DeepSpeed) → checkpoints to S3 every N steps
        metrics (loss, eval loss) → metrics store → streamed to UI
   → Eval gate: run the customer's validation set + standard safety evals; compare against the base model
   → Artifact registry (adapter/weights, versioned, lineage: dataset hash, base model, hyperparameters)
   → Deploy: LoRA adapter loaded onto shared serving pools (cheap) or a dedicated endpoint for full fine-tunes
```

## 3. Deep dives
- **LoRA vs full fine-tuning:** LoRA trains about 0.1–1% of the parameters. It's cheap, the adapters are small (MBs), and many adapters can share one base model when serving. Full fine-tuning gives the best quality at a high cost.
- **Scheduling:** gang scheduling (all GPUs for a job start together), bin-packing small jobs, fair-share quotas, preemptible tiers with checkpoint/resume.
- **Fault tolerance:** GPU failures are common on long jobs, so checkpoint frequently and auto-resume from the latest checkpoint on a healthy node.
- **Data isolation and privacy:** per-tenant encryption keys, no cross-tenant caching, training data deleted per the retention policy, and the base model is never updated with customer data.
- **Safety:** fine-tuning can remove safety behavior, so run safety evals before deployment and block models that fail.
- **Cost estimation and billing:** tokens × epochs × price; show the estimate before the job starts.
- **Reproducibility:** pin the base model, code version, random seed, and dataset hash.

## ✅ Takeaways
Validation → GPU-aware scheduler → checkpointed training → **eval and safety gate** → registry → LoRA multiplexed serving. Emphasize tenant isolation and fault tolerance.
