# Step 13 of 13: Putting It All Together (millions of users)

[🏠 Overview](README.md) · **← Prev** [Step 12](12_database_sharding.md)

## 🏁 The final architecture
```
                                   Users (web / mobile)
                                          │
                     ┌────────────────────┼─────────────────────┐
                     ▼                    ▼                     │
         [Step 7] CDN edge ◀── S3      GeoDNS [Step 9]          │
              (static/media)              │ nearest healthy DC   │
                                          ▼                     ▼
  ┌────────────────────────── DATA CENTER / REGION 1 ──────────────────────┐   ┌── REGION 2 ──┐
  │  [Step 4] Load balancer (multi-AZ)                                      │   │ (same stack) │
  │            │                                                            │   │              │
  │  [Steps 3+8] Stateless web/app servers (autoscaled) ── session store    │   │              │
  │            │                     │                                      │   │              │
  │  [Step 6] Cache cluster (Redis)  │ [Step 10] Message queue ──▶ Workers  │   │              │
  │            │                     │                                      │   │              │
  │  [Steps 2+5+12] DB shards, each = primary + replicas ◀══ async replication ══▶ │           │
  │                                                                         │   │              │
  │  [Step 11] Logging · metrics · tracing · alerting · CI/CD · IaC         │   │              │
  └─────────────────────────────────────────────────────────────────────────┘   └──────────────┘
```

## 📋 Recap: problem → component (memorize this table)
| # | Problem | Component | Key idea |
|---|---|---|---|
| 1 | Need to serve users | Server + DNS | DNS maps name → IP |
| 2 | App and DB compete | Separate DB tier | Scale tiers independently; SQL by default |
| 3 | Out of capacity | Horizontal scaling | More machines > a bigger machine |
| 4 | Distribute traffic, survive failures | Load balancer | Health checks, failover, private IPs |
| 5 | DB is a SPOF and read-bound | Replication | Primary for writes, replicas for reads, failover |
| 6 | Repeated expensive reads | Cache | In-memory, cache-aside, TTL, invalidation |
| 7 | Far-away users, static load | CDN | Edge copies, versioned filenames |
| 8 | Sessions stuck on servers | Stateless tier | State in a shared store, so autoscaling works |
| 9 | Region outages, global latency | Multiple data centers | GeoDNS, replication, failover |
| 10 | Slow tasks, coupling, spikes | Message queue | Async workers, retries, idempotency |
| 11 | Can't see or deploy safely | Observability + automation | Logs, metrics, tracing, CI/CD, IaC |
| 12 | Writes and data outgrow one DB | Sharding | Shard key, resharding, hot keys, denormalization |

## 🎯 Summary principles for scaling
- Keep the **web tier stateless**.
- Build **redundancy at every tier** (no single point of failure).
- **Cache** data as much as you can.
- Support **multiple data centers**.
- Host static assets on a **CDN**.
- Scale the **data tier by sharding** (only when you have to).
- Split tiers into **individual services** as teams and load grow.
- **Monitor** everything and **automate** deployments.

## 🧪 The 10-minute drill (do this until it's automatic)
Blank page. Timer for 10 minutes. Starting from one server, **add each component in order, saying out loud which problem it fixes.** This is the answer to "scale to millions of users" and the opening of almost every other HLD question.

## ➡️ Where to go next
1. **Concept depth:** the [topic modules 01–10](../README.md#-concept-modules) cover each component in detail.
2. **The framework:** [how to run a 45-minute design interview](../11_interview_framework/).
3. **Quick reference:** [HLD cheat sheet](../00_hld_cheatsheet.md).
4. **Practice:** start with 🟢 [URL shortener](../12_problems/easy/01_url_shortener_pastebin.md) and [Scale on AWS](../12_problems/easy/04_scale_to_millions_aws.md), then work through [all 29 problems](../12_problems/README.md).
5. **Beyond Step 12** (each is a chapter-level topic, and each has a problem here): [rate limiter](../12_problems/easy/02_rate_limiter.md) · [consistent hashing](../03_load_balancing_reverse_proxy/) · [key-value store](../12_problems/hard/17_distributed_kv_store.md) · [unique ID generator](../12_problems/easy/05_unique_id_generator.md) · [URL shortener](../12_problems/easy/01_url_shortener_pastebin.md) · [web crawler](../12_problems/medium/07_web_crawler.md) · [notification system](../12_problems/medium/09_notification_system.md) · [news feed](../12_problems/medium/06_twitter_news_feed.md) · [chat](../12_problems/medium/08_chat_system.md) · [autocomplete](../12_problems/medium/10_typeahead_autocomplete.md) · [YouTube](../12_problems/hard/15_youtube_video_streaming.md) · [Google Drive](../12_problems/medium/22_dropbox_file_sync.md)
