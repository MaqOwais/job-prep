# 🗺️ High-Level Design (HLD) Cheat Sheet

**HLD vs LLD:**
- **High-level design** (this folder): services, data stores, queues, caches, how they connect, and how the system scales and fails. Boxes and arrows.
- **Low-level design** ([03_low_level_design](../03_low_level_design/)): classes, interfaces, and methods inside one component. Code.

Read this page before every mock. It's the one-page summary of everything in 01–11.

---

## 1. The universal HLD skeleton (start every diagram from this)
```
                        ┌──────────── CDN (static/media) ◀── Object storage (S3)
Clients (web/mobile) ───┤
                        └─▶ DNS ─▶ Load balancer (L7) ─▶ API gateway (auth, rate limit, routing)
                                                         │
                     ┌───────────────────┬───────────────┼────────────────────┐
                     ▼                   ▼               ▼                    ▼
               Service A (stateless) Service B      Service C          WebSocket gateway (real-time)
                     │                   │               │
              Cache (Redis)         Cache            Message queue / stream (Kafka/SQS)
                     │                   │               │
              SQL DB (primary +    NoSQL DB          Async workers ─▶ Search index / Analytics / Notifications
              replicas, sharded)  (Cassandra/Dynamo)
Cross-cutting: service discovery · config · monitoring/logging/tracing · secrets · CI/CD · multi-AZ/region
```
Then **remove what you don't need** and **zoom into what matters** for the specific problem.

---

## 2. Component catalog: when to reach for what
| Need | Component | Concrete examples | Say this |
|---|---|---|---|
| Spread traffic, remove SPOFs | **Load balancer** | ALB/NLB, NGINX, HAProxy | "L7 LB across 3 AZs, health checks, stateless servers behind it" |
| One entry point for auth, throttling, routing | **API gateway** | Kong, AWS API Gateway, Envoy | "Gateway handles JWT validation and per-user rate limits" |
| Serve static or media files fast, globally | **CDN** | CloudFront, Cloudflare, Akamai | "Media served from the CDN; the origin only sees cache misses" |
| Store files and blobs | **Object storage** | S3, GCS | "Upload directly to S3 with a pre-signed URL so the bytes skip our servers" |
| Transactions, relations, strong consistency | **Relational DB** | Postgres, MySQL, Aurora | "Orders and payments in Postgres for ACID" |
| Massive write throughput, simple access patterns | **Wide-column / KV store** | Cassandra, DynamoDB, ScyllaDB | "Messages partitioned by conversation_id, clustered by time" |
| Flexible documents | **Document DB** | MongoDB, DynamoDB | "Product catalog with varying attributes" |
| Relationship traversal | **Graph DB** | Neo4j, Neptune | "Friend-of-friend queries" |
| Fast reads of hot data | **Cache** | Redis, Memcached | "Cache-aside, TTL with jitter, delete on write" |
| Full-text search | **Search index** | Elasticsearch / OpenSearch | "CDC from the DB into Elasticsearch" |
| Rankings, counters, sets | **Redis data structures** | Sorted sets, HyperLogLog, INCR | "Leaderboard in a Redis sorted set" |
| Decouple, buffer spikes, async jobs | **Message queue** | SQS, RabbitMQ | "Upload returns 202; workers process from the queue" |
| Event streams, replay, fan-out to many consumers | **Log / stream** | Kafka, Kinesis, Pulsar | "Events to Kafka, partitioned by user_id for ordering" |
| Real-time push to clients | **WebSocket / SSE gateway** | Socket servers + Redis pub/sub | "Session registry maps user → gateway node" |
| Coordination, leader election, locks | **Coordination service** | ZooKeeper, etcd | "Leader election for the scheduler via etcd lease" |
| Workflows with retries | **Workflow engine** | Step Functions, Temporal, Airflow | "Saga orchestrated by Temporal" |
| Analytics over huge data | **Data warehouse / lake** | Redshift, BigQuery, S3 + Athena, Spark | "Nightly batch to the warehouse; dashboards don't hit OLTP" |
| Real-time aggregation | **Stream processor** | Flink, Kafka Streams, Spark Streaming | "Flink computes 1-minute windows" |
| Time-series metrics | **TSDB** | Prometheus, InfluxDB, Timestream | "Downsample old data" |
| Geospatial queries | **Geo index** | Geohash, quadtree, H3, PostGIS, Redis GEO | "Drivers indexed by geohash cell" |
| Unique, sortable IDs | **ID generator** | Snowflake, ULID | "Snowflake IDs double as time-ordered cursors" |
| Approximate counting / membership | **Probabilistic structures** | Bloom filter, HyperLogLog, Count-Min Sketch | "Bloom filter for seen URLs" |

---

## 3. Scaling playbook (problem → fix)
| Symptom | Fix (in rough order) |
|---|---|
| App servers overloaded | Horizontal scaling + LB + stateless design + autoscaling |
| DB reads overloaded | Cache → read replicas → CDN for static content → denormalize |
| DB writes overloaded | Batch writes, async queue → shard → switch to an LSM-tree store |
| Hot key / celebrity | Key splitting, local cache, request coalescing, a special path for hot entities |
| Slow requests | Move work async, precompute, add caching, parallelize calls |
| Spiky traffic | Queue as a buffer, autoscaling, rate limiting, back pressure |
| Global latency | CDN, edge caching, multi-region with GeoDNS, regional data |
| Large files | Chunking, multipart/resumable upload, direct-to-object-storage, CDN |
| Too many connections | Connection pooling, WebSocket gateways, event-loop servers |
| Big fan-out | Fan-out on write for most users + fan-out on read for heavy hitters |

## 4. Reliability playbook
Redundancy across AZs · replication + automatic failover · retries with **exponential backoff + jitter** · **timeouts** everywhere · **circuit breakers** · **idempotency keys** · DLQs · graceful degradation (serve stale data, turn off non-critical features) · bulkheads · health checks · chaos testing · backups + tested restores · RPO/RTO targets.

## 5. Consistency cheat sheet
| Data | Typical choice |
|---|---|
| Money, inventory, bookings, unique usernames | **Strong** (SQL transactions, conditional writes, locks) |
| Feeds, likes, view counts, recommendations | **Eventual** (async, caches, counters) |
| Chat messages | Ordered per conversation; at-least-once + client dedup |
| User profile after edit | Read-your-writes (read from the primary or a session-pinned replica) |

---

## 6. Tradeoff phrase bank (say these out loud)
- "This is a **read-heavy** system (~100:1), so I'll optimize the read path with caching and precomputation."
- "I'm choosing **availability over consistency** here because a stale like count is harmless."
- "For bookings I need **strong consistency**, so I'll use a transactional DB with a conditional update to prevent double-booking."
- "**Fan-out on write** makes reads O(1) but is expensive for celebrities, so I'll use a hybrid."
- "I'll make the consumer **idempotent**, since the queue gives at-least-once delivery."
- "We could shard by user_id or by time. user_id keeps one user's data together, but risks hot shards for power users. I'd mitigate that with…"
- "To keep the first version simple I'd start with X. At 10× scale I'd move to Y."
- "The **bottleneck** here is going to be… Let me deep-dive on that."

## 7. Numbers to have ready
1 day ≈ 10⁵ s · 1M/day ≈ 12/s · peak ≈ 2–3× average · Redis ~100K ops/s per node · a single SQL node ~1–10K writes/s · cross-region round trip ~100–150 ms · same-datacenter ~0.5 ms · SSD read ~100 µs. More in [estimation](10_estimation/).

---

## 8. Most-asked HLD questions by company (as commonly reported; use these to prioritize)
| Company | Frequently reported questions | In this repo |
|---|---|---|
| **Amazon / AWS** | Distributed KV store, e-commerce checkout, rate limiter, notification system, recommendation system, URL shortener | [17](12_problems/hard/17_distributed_kv_store.md) · [24](12_problems/medium/24_ecommerce_checkout.md) · [02](12_problems/easy/02_rate_limiter.md) · [09](12_problems/medium/09_notification_system.md) · [AI 07](../08_ai_system_design/problems/medium/07_recommendation_system.md) |
| **Google** | Search/typeahead, YouTube, Google Docs, web crawler, Maps/proximity | [10](12_problems/medium/10_typeahead_autocomplete.md) · [15](12_problems/hard/15_youtube_video_streaming.md) · [18](12_problems/hard/18_google_docs.md) · [07](12_problems/medium/07_web_crawler.md) · [25](12_problems/medium/25_proximity_service_yelp.md) |
| **Meta** | News feed, Instagram, Messenger, live comments, top-K / leaderboard | [06](12_problems/medium/06_twitter_news_feed.md) · [21](12_problems/medium/21_instagram.md) · [08](12_problems/medium/08_chat_system.md) · [20](12_problems/easy/20_leaderboard.md) |
| **Microsoft** | Teams/chat, OneDrive/Dropbox, notification system, job scheduler | [08](12_problems/medium/08_chat_system.md) · [22](12_problems/medium/22_dropbox_file_sync.md) · [26](12_problems/hard/26_distributed_job_scheduler.md) |
| **Uber / Lyft / DoorDash** | Ride matching, proximity, payments, ETA | [16](12_problems/hard/16_uber_ride_sharing.md) · [25](12_problems/medium/25_proximity_service_yelp.md) · [19](12_problems/hard/19_payment_system.md) |
| **Netflix** | Video streaming, recommendations, metrics/monitoring | [15](12_problems/hard/15_youtube_video_streaming.md) · [27](12_problems/hard/27_metrics_monitoring.md) |
| **Stripe / fintech** | Payment system, idempotent APIs, ledger, rate limiter | [19](12_problems/hard/19_payment_system.md) · [02](12_problems/easy/02_rate_limiter.md) |
| **Ticketing / booking** | Ticketmaster, hotel booking, flash sales | [23](12_problems/medium/23_ticketmaster.md) |
| **Infra / data roles** | Kafka-like queue, metrics system, scheduler, distributed cache | [28](12_problems/hard/28_distributed_message_queue.md) · [27](12_problems/hard/27_metrics_monitoring.md) · [26](12_problems/hard/26_distributed_job_scheduler.md) · [03](12_problems/easy/03_key_value_cache.md) |
| **Trading firms** | Stock exchange / order matching | [29](12_problems/hard/29_stock_exchange.md) |
| **AI companies** | RAG, LLM gateway, inference platform, agents | [08_ai_system_design](../08_ai_system_design/) |
