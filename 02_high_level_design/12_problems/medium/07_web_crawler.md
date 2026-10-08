# 🟡 07. Web Crawler

📖 Primer solution: [Design a web crawler](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** start from seed URLs, fetch pages, extract links, store content for indexing, recrawl periodically.
**Non-functional:** scale (1B pages/month), **politeness** (don't overload sites, respect robots.txt), robustness (bad HTML, crawler traps), dedup, extensibility.

## 2. Estimates
1B pages/month → ~400 pages/s. 500 KB/page → **500 TB/month** of raw content (compressed is much less).

## 3. High-level design
```
Seed URLs → URL Frontier (priority + politeness queues)
              │
              ▼
          Fetcher workers ── DNS resolver (cached)
              │  (robots.txt cache)
              ▼
          Content parser → content dedup (hash/SimHash) → Content store (S3) → Indexer
              │
              ▼
          Link extractor → URL filter → URL-seen check (Bloom filter + DB) → back to Frontier
```

## 4. Deep dives
**URL frontier (the core component):**
- **Front queues:** prioritized by PageRank, freshness, or change frequency.
- **Back queues:** **one queue per host**, plus a heap of "next allowed fetch time per host". This is how you enforce politeness (e.g. 1 request/s per domain).

**Dedup:**
- URL-seen: normalize the URL (lowercase, strip fragments, sort query params) → **Bloom filter** (memory-efficient, no false negatives) + a persistent store.
- Content-seen: checksum for exact duplicates, **SimHash/MinHash** for near-duplicates.

**Robustness:**
- Crawler traps (infinite calendars, session IDs in URLs) → max depth, max URL length, per-domain page caps.
- Timeouts and retries with backoff; skip non-HTML content types.

**Distribution:** partition the frontier by **hash(hostname)**, so all URLs for a host go to the same worker, which keeps politeness local.

**Recrawl:** schedule by change frequency (news sites hourly, static pages monthly).

## 5. Data stores
- Frontier: Kafka or Redis queues, persisted.
- Seen URLs: Bloom filter + RocksDB/Cassandra.
- Content: S3 (compressed) + metadata in Bigtable/Cassandra.

## ✅ Takeaways
Frontier with **per-host politeness queues**, **Bloom filter dedup**, trap handling, and partitioning by hostname.
