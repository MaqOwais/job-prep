# 🧪 System Design Problems: Easy → Medium → Hard

**How to use each problem:**
1. Read only the title + requirements. Close the file.
2. Design it yourself in **35 minutes** using the [framework](../11_interview_framework/).
3. Open the notes and compare. Then read the primer solution (📖), if there is one.
4. Write down 3 things you missed. Redo it from memory 3 days later.

Every problem file follows the same structure: Requirements → Estimates → API → Data model → High-level design → Deep dives → Bottlenecks → Follow-ups.

## 🟢 Easy: one main idea each
| # | Problem | Core concepts it teaches | Primer solution |
|---|---|---|---|
| 01 | [URL shortener / Pastebin](easy/01_url_shortener_pastebin.md) | Hashing/base62, read-heavy caching, KV store | [📖 Pastebin](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md) |
| 02 | [Rate limiter](easy/02_rate_limiter.md) | Token bucket, sliding window, Redis atomics | — |
| 03 | [Key-value cache (search query cache)](easy/03_key_value_cache.md) | LRU, sharding the cache, consistent hashing | [📖 Query cache](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md) |
| 04 | [Scale to millions of users on AWS](easy/04_scale_to_millions_aws.md) | Iterative scaling: 1 box → multi-AZ → caches → autoscaling | [📖 Scaling AWS](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md) |
| 05 | [Unique ID generator](easy/05_unique_id_generator.md) | Snowflake IDs, clock skew | — |

## 🟡 Medium: several components + one hard tradeoff
| # | Problem | Core concepts | Primer solution |
|---|---|---|---|
| 06 | [Twitter / news feed](medium/06_twitter_news_feed.md) | Fan-out on write vs read, celebrity problem | [📖 Twitter](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md) |
| 07 | [Web crawler](medium/07_web_crawler.md) | URL frontier, politeness, dedup, Bloom filter | [📖 Web crawler](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md) |
| 08 | [Chat system (WhatsApp)](medium/08_chat_system.md) | WebSockets, presence, message ordering, offline delivery | — |
| 09 | [Notification system](medium/09_notification_system.md) | Queues, retries, templates, user preferences, dedup | — |
| 10 | [Typeahead / autocomplete](medium/10_typeahead_autocomplete.md) | Trie with top-k, offline aggregation | — |
| 11 | [Social graph (friends of friends)](medium/11_social_graph.md) | Graph sharding, BFS across services | [📖 Social graph](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md) |
| 12 | [Sales rank by category (Amazon)](medium/12_sales_rank.md) | Batch MapReduce, top-k | [📖 Sales rank](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md) |
| 13 | [Personal finance (Mint)](medium/13_mint_personal_finance.md) | Async ingestion, categorization, budgets | [📖 Mint](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md) |
| 14 | [Search engine](medium/14_search_engine.md) | Inverted index, ranking, sharding the index | — |

## 🔴 Hard: distributed systems depth
| # | Problem | Core concepts |
|---|---|---|
| 15 | [YouTube / video streaming](hard/15_youtube_video_streaming.md) | Transcoding pipeline, adaptive bitrate, CDN |
| 16 | [Uber / ride sharing](hard/16_uber_ride_sharing.md) | Geospatial indexing, real-time matching, location updates |
| 17 | [Distributed key-value store (Dynamo)](hard/17_distributed_kv_store.md) | Consistent hashing, quorum, vector clocks, gossip |
| 18 | [Google Docs](hard/18_google_docs.md) | OT/CRDT, real-time sync, versioning |
| 19 | [Payment system](hard/19_payment_system.md) | Idempotency, ledgers, exactly-once, reconciliation |
| 20 | [LLM / RAG platform](hard/20_llm_rag_platform.md) | Embeddings, vector search, GPU serving, streaming, guardrails |

## More practice questions
The primer's [additional system design interview questions](https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions) list includes Dropbox, Google search, a distributed lock, an API rate limiter, a stock exchange, and more, each linked to real articles.
