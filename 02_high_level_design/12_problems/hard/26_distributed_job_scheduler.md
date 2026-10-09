# 🔴 26. Distributed Job Scheduler (cron at scale / Airflow-like)

📖 Related: [Asynchronism & queues](../../07_asynchronism_queues/) · [Unique IDs](../easy/05_unique_id_generator.md)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** schedule jobs to run once at a time T, or on a recurring cron schedule; jobs can have dependencies (a DAG); retries with backoff; check status and logs; cancel.
**Non-functional:** millions of scheduled jobs, run **on time** (within seconds), **at least once and preferably exactly once**, no single point of failure, scale horizontally.

## 2. High-level design
```
Client → Job API → Jobs DB (SQL: job definitions, schedules, DAG, owner) 
                   Schedule table: (next_run_at, job_id) indexed by next_run_at, partitioned into N shards
SCHEDULERS (many nodes; each OWNS a set of shards via leases in etcd/ZooKeeper):
     every second: SELECT due jobs WHERE next_run_at <= now() AND shard IN (mine) LIMIT k
     → create Execution (exec_id, job_id, scheduled_time) with UNIQUE(job_id, scheduled_time)  ← dedup!
     → enqueue to Kafka/SQS (by priority/queue) → compute & update next_run_at (cron parse)
WORKERS (autoscaled pools): pull task → heartbeat while running → run in container/sandbox
     → report SUCCEEDED/FAILED → retries with backoff; DLQ after max attempts
Status/logs → Executions DB + log storage (S3) → UI/API
```

## 3. Deep dives
- **Finding due jobs efficiently:** an index on `next_run_at`, partitioned so that every scheduler scans only its shards. Alternatives: a time-bucketed table (one row per minute bucket), or Redis sorted sets keyed by timestamp (`ZRANGEBYSCORE`).
- **No double-firing:** shard ownership through **leases** (a lease expires if the scheduler dies → another node takes over) + a **unique constraint on (job_id, scheduled_time)**, so even if two schedulers race, only one execution is created.
- **Exactly-once is impossible end to end:** use at-least-once delivery + **idempotent jobs** (pass the exec_id as an idempotency key).
- **Worker failure:** heartbeats/visibility timeouts. A missed heartbeat → the task is re-queued.
- **DAGs:** a downstream task is enqueued only after all its upstream tasks succeed (track dependency counts, as in topological sort, see [coding: graphs](../../../01_coding/11_graphs/)).
- **Hot minute:** many jobs at 00:00 → add jitter, spread across shards, autoscale the workers.
- **Missed runs after an outage:** policy per job: catch up on all missed runs, run only the latest, or skip.
- **Multi-tenancy:** per-tenant quotas, priority queues, isolated worker pools.

## ✅ Takeaways
Indexed `next_run_at` + **sharded schedulers with leases** + a **unique (job, time)** dedup constraint + queue + heartbeating workers + idempotent jobs.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do schedulers find due jobs efficiently?</b></summary>

An **index on next_run_at** (partitioned into shards), queried with WHERE next_run_at <= now() for owned shards. Alternatives: time-bucketed tables (one row per minute bucket) or Redis sorted sets scored by timestamp (ZRANGEBYSCORE).

</details>

<details>
<summary><b>Q2. How do you prevent two schedulers from firing the same job?</b></summary>

**Shard ownership via leases** (etcd/ZooKeeper), so each shard has one active scheduler, plus a **unique constraint on (job_id, scheduled_time)** in the executions table, so even a race creates only one execution.

</details>

<details>
<summary><b>Q3. A worker dies while running a job. What happens?</b></summary>

Workers **heartbeat** while running. If heartbeats stop (or a visibility timeout expires), the execution is marked failed or lost and **re-queued** for another worker, subject to the retry policy. Jobs must be **idempotent** because they can run twice.

</details>

<details>
<summary><b>Q4. How do you run a DAG of dependent tasks?</b></summary>

Track each task's **pending upstream count** (topological order). When a task succeeds, decrement its children's counts, and enqueue any child that reaches zero. A failure triggers retries, then marks the downstream tasks as skipped or failed according to the policy.

</details>

<details>
<summary><b>Q5. What if thousands of jobs are scheduled for exactly midnight?</b></summary>

Add **jitter** where the exact time doesn't matter, spread the jobs across shards, pre-scale workers before known peaks, and use priority queues so critical jobs aren't stuck behind bulk ones.

</details>
