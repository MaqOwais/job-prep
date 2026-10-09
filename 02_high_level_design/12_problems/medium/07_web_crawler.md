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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How does the crawler stay polite to websites?</b></summary>

Respect **robots.txt** (cached per host), and keep **per-host queues** with a minimum delay between requests to the same host (tracked in a heap of next-allowed fetch times). Identify the crawler in its User-Agent, and back off on 429/5xx responses.

</details>

<details>
<summary><b>Q2. How do you avoid crawling the same URL twice?</b></summary>

**Normalize** URLs (lowercase host, remove fragments, sort query params, resolve relative paths), then check a **Bloom filter** (memory-efficient, no false negatives) backed by a persistent seen-URL store. Detect duplicate **content** with checksums or SimHash.

</details>

<details>
<summary><b>Q3. What are crawler traps, and how do you avoid them?</b></summary>

Infinite URL spaces such as calendars that go on forever, session IDs in URLs, and endlessly deep links. Defenses: maximum depth, maximum URL length, per-domain page budgets, pattern blacklists, and detecting near-duplicate content.

</details>

<details>
<summary><b>Q4. How do you distribute the crawl across many machines?</b></summary>

Partition the URL frontier by **hash(hostname)**, so each host is owned by one worker. That keeps politeness and robots.txt logic local and avoids cross-node coordination. Workers share a seen-URL store and DNS cache.

</details>

<details>
<summary><b>Q5. How do you decide what to recrawl, and how often?</b></summary>

Prioritize by **importance** (PageRank, traffic) and **change frequency** learned from history: news homepages every few minutes, static pages monthly. Use HTTP conditional requests (ETag / If-Modified-Since) to cut the cost of unchanged pages.

</details>
