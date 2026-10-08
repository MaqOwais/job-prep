# 🔴 27. Metrics Monitoring & Alerting System (Datadog / Prometheus / CloudWatch)

📖 Related: [Asynchronism & queues](../../07_asynchronism_queues/) · [Prometheus architecture](https://prometheus.io/docs/introduction/overview/) · [Gorilla TSDB paper (Facebook)](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** collect metrics (CPU, latency, request counts, custom metrics) from 100K+ hosts; dashboards with queries over time ranges; alert rules ("p99 latency > 500 ms for 5 min") → notify on-call.
**Non-functional:** **write-heavy** (millions of data points/s), fast queries on recent data, retention of 1 year (lower resolution for old data), alerts within about a minute. The monitoring system must be **more reliable than what it monitors**.

## 2. Estimates
100K hosts × 100 metrics × 1 sample/10 s = **1M points/s**. Each point is ~16 B raw, ~1.4 B with Gorilla compression → about 120 GB/day compressed.

## 3. Data model
`metric_name{label1=v1, label2=v2}` → series of `(timestamp, value)`.
**Cardinality** = the number of unique label combinations. High cardinality (e.g., user_id as a label) is the #1 thing that breaks a TSDB.

## 4. High-level design
```
Hosts: agent (collect, pre-aggregate, buffer) ──push──▶ Ingestion gateways (LB, auth, validation)
   (or Prometheus-style PULL: scrapers discover targets via service discovery)
        → Kafka (buffer; decouples ingestion from storage; replay)
        → Stream processors: rollups (1m, 1h), alert evaluation on hot data
        → TSDB storage nodes (sharded by series hash; replicated)
              in-memory head block (recent 2h) → compressed immutable blocks on disk → object storage (S3) for old data
              downsampling: raw 7d → 1-min 30d → 1-hour 1y
Query service: parse query (PromQL-like) → fan out to shards → merge/aggregate → cache → Dashboards (Grafana)
Alerting: rule evaluator (every 30–60s) → state machine (pending → firing → resolved) → dedup/group/silence
          → notification router → PagerDuty/Slack/email
Meta-monitoring: a separate, simple system watches the monitoring system ("who watches the watchers")
```

## 5. Deep dives
- **Push vs pull:** pull (Prometheus) makes target health visible and is easy for servers. Push suits short-lived jobs, serverless, and clients behind NAT.
- **Why a specialized TSDB:** time-ordered appends, **delta-of-delta timestamps + XOR value compression (Gorilla)**, columnar blocks, and a label inverted index for lookups.
- **Kafka buffer:** absorbs spikes and protects storage during outages.
- **Downsampling and retention** keep storage cost and query time bounded.
- **Alert quality:** `for:` durations to avoid flapping, grouping and dedup, silences, routing by team and severity. Alert on **symptoms** (SLOs) rather than causes.
- **Query performance:** pre-aggregated rollups, query result caching, limits on cardinality and time range.

## ✅ Takeaways
Agents → **Kafka buffer** → sharded **TSDB with compression and downsampling** → query fan-out; alert state machine with dedup; watch the cardinality.
