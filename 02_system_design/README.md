# 🏗️ System Design

This section follows the structure of the [System Design Primer](https://github.com/donnemartin/system-design-primer) (CC BY 4.0). Each module has my **condensed notes + interview phrasing + links to the exact primer sections** for more depth.

## How to study (easy → hard)
1. **Concepts (Weeks 1–2):** read modules 1–10 in order. After each one, explain it out loud in 2 minutes without notes.
2. **Framework:** learn [11_interview_framework](11_interview_framework/) by heart. Every design answer follows it.
3. **Problems (Weeks 3–6):** 🟢 easy → 🟡 medium → 🔴 hard. For each one: try it yourself for 35 minutes on paper or [Excalidraw](https://excalidraw.com) **first**, then compare against the notes and the primer solution.
4. **Flashcards:** primer [Anki decks](https://github.com/donnemartin/system-design-primer#anki-flashcards) (system design + exercises), 10 minutes a day.

## 📚 Concept modules
| # | Module | Primer sections |
|---|---|---|
| 1 | [Fundamentals](01_fundamentals/): scalability, latency/throughput, CAP, consistency, availability | [Performance vs scalability](https://github.com/donnemartin/system-design-primer#performance-vs-scalability) · [CAP](https://github.com/donnemartin/system-design-primer#cap-theorem) · [Consistency](https://github.com/donnemartin/system-design-primer#consistency-patterns) · [Availability](https://github.com/donnemartin/system-design-primer#availability-patterns) |
| 2 | [DNS & CDN](02_dns_cdn/) | [DNS](https://github.com/donnemartin/system-design-primer#domain-name-system) · [CDN](https://github.com/donnemartin/system-design-primer#content-delivery-network) |
| 3 | [Load balancing & reverse proxy](03_load_balancing_reverse_proxy/) | [Load balancer](https://github.com/donnemartin/system-design-primer#load-balancer) · [Reverse proxy](https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server) |
| 4 | [Application layer & microservices](04_application_layer_microservices/) | [Application layer](https://github.com/donnemartin/system-design-primer#application-layer) |
| 5 | [Databases](05_databases/): SQL, replication, sharding, NoSQL | [Database](https://github.com/donnemartin/system-design-primer#database) |
| 6 | [Caching](06_caching/) | [Cache](https://github.com/donnemartin/system-design-primer#cache) |
| 7 | [Asynchronism & queues](07_asynchronism_queues/) | [Asynchronism](https://github.com/donnemartin/system-design-primer#asynchronism) |
| 8 | [Communication protocols](08_communication_protocols/): HTTP, TCP/UDP, RPC, REST | [Communication](https://github.com/donnemartin/system-design-primer#communication) |
| 9 | [Security](09_security/) | [Security](https://github.com/donnemartin/system-design-primer#security) |
| 10 | [Estimation](10_estimation/): back-of-envelope numbers | [Appendix](https://github.com/donnemartin/system-design-primer#appendix) |
| 11 | [Interview framework](11_interview_framework/) | [How to approach a system design interview](https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question) |

## 🧪 Design problems
See [12_problems/README.md](12_problems/README.md) for the full list, ordered by difficulty.

| 🟢 Easy | 🟡 Medium | 🔴 Hard |
|---|---|---|
| [URL shortener / Pastebin](12_problems/easy/01_url_shortener_pastebin.md) | [Twitter / news feed](12_problems/medium/06_twitter_news_feed.md) | [YouTube](12_problems/hard/15_youtube_video_streaming.md) |
| [Rate limiter](12_problems/easy/02_rate_limiter.md) | [Web crawler](12_problems/medium/07_web_crawler.md) | [Uber](12_problems/hard/16_uber_ride_sharing.md) |
| [Key-value cache](12_problems/easy/03_key_value_cache.md) | [Chat system](12_problems/medium/08_chat_system.md) | [Distributed KV store](12_problems/hard/17_distributed_kv_store.md) |
| [Scale to millions on AWS](12_problems/easy/04_scale_to_millions_aws.md) | [Notification system](12_problems/medium/09_notification_system.md) | [Google Docs](12_problems/hard/18_google_docs.md) |
| [Unique ID generator](12_problems/easy/05_unique_id_generator.md) | [Typeahead](12_problems/medium/10_typeahead_autocomplete.md) | [Payment system](12_problems/hard/19_payment_system.md) |
| | [Social graph](12_problems/medium/11_social_graph.md) | [LLM / RAG platform](12_problems/hard/20_llm_rag_platform.md) |
| | [Sales rank](12_problems/medium/12_sales_rank.md) | |
| | [Mint](12_problems/medium/13_mint_personal_finance.md) | |
| | [Search engine](12_problems/medium/14_search_engine.md) | |

## 🧩 The building blocks (one-line reminders)
| Problem | Building block |
|---|---|
| Too many reads | Cache (Redis), read replicas, CDN |
| Too many writes | Sharding, write-behind queue, LSM-tree DB (Cassandra) |
| Slow tasks | Message queue + async workers |
| Single point of failure | Redundancy + failover, multi-AZ |
| Global users | CDN, GeoDNS, multi-region |
| Uneven load | Load balancer, consistent hashing |
| Search | Inverted index (Elasticsearch) |
| Real-time push | WebSockets, SSE, long polling |
| Unique IDs | Snowflake IDs |
| Exactly-once side effects | Idempotency keys |
| Hot keys | Key splitting, local cache, request coalescing |

## 🔗 Other great resources
- [ByteByteGo / Alex Xu, *System Design Interview* Vol 1 & 2](https://bytebytego.com/): problem walkthroughs
- [Designing Data-Intensive Applications (Kleppmann)](https://dataintensive.net/): the deep theory book
- [Hello Interview: system design](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction): modern, interview-focused
- Primer: [Real-world architectures](https://github.com/donnemartin/system-design-primer#real-world-architectures) · [Company engineering blogs](https://github.com/donnemartin/system-design-primer#company-engineering-blogs) · [Additional interview questions](https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions)
