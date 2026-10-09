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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. LoRA vs full fine-tuning?</b></summary>

**LoRA** trains small low-rank adapter matrices (~0.1–1% of the parameters): cheap, fast, small artifacts (MBs), and many adapters can share one base model at serving time. **Full fine-tuning** updates all weights: the best quality ceiling, but expensive training and serving (a whole model copy per customer).

</details>

<details>
<summary><b>Q2. How do you schedule many training jobs on a shared GPU cluster?</b></summary>

A GPU-aware scheduler with **gang scheduling** (all GPUs for a job start together), bin-packing of small jobs, **per-tenant quotas and priorities**, preemption of low-priority jobs (with checkpoints), and topology awareness (keep multi-GPU jobs on one node or fast interconnect).

</details>

<details>
<summary><b>Q3. How do you survive GPU failures during a 20-hour training run?</b></summary>

**Checkpoint frequently** to object storage (model + optimizer state + data position), detect failed nodes via health checks, and **automatically resume** from the last checkpoint on healthy hardware. Track the effective training time lost.

</details>

<details>
<summary><b>Q4. Why add an evaluation gate before deployment?</b></summary>

Fine-tuning can **degrade quality or remove safety behavior**. Run the customer's validation set + standard capability and **safety evals**, compare against the base model, and block or flag models that regress or fail safety thresholds.

</details>

<details>
<summary><b>Q5. How do you keep each customer's training data isolated?</b></summary>

Separate storage prefixes or buckets with **per-tenant encryption keys**, no shared caches, isolated job containers, a strict IAM scope per job, data deletion per the retention policy, and never feeding customer data into shared base models.

</details>
