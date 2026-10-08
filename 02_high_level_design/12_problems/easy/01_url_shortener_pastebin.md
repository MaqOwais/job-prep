# 🟢 01. URL Shortener / Pastebin (bit.ly, pastebin.com)

📖 Primer solution: [Design Pastebin.com (or Bit.ly)](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** shorten a long URL (or paste text) → short link; redirect or show the content; optional custom alias and expiration; basic click analytics.
**Non-functional:** very **read-heavy** (100:1), low-latency redirects, highly available, links must not collide, and links shouldn't be guessable (optional).

## 2. Estimates
- 100M new URLs/month → ~40 writes/s. Reads at 100× → ~4,000 reads/s (peak ~10K).
- Over 10 years: 100M × 12 × 10 = 12B URLs × ~500 B ≈ **6 TB**.
- Key length: base62 (`[a-zA-Z0-9]`). 62⁷ ≈ 3.5 trillion, so **7 characters** is enough.

## 3. API
```
POST /v1/urls   {long_url, custom_alias?, expire_at?}  → 201 {short_url}
GET  /{code}                                           → 301/302 Location: long_url
```
**301 (permanent)** is cached by browsers, which reduces load but means you **lose analytics**. **302 (temporary)** sends every click to the server, which keeps analytics.

## 4. Data model
`urls(code PK, long_url, user_id, created_at, expire_at)`. A simple key lookup, so use a **KV store / DynamoDB / Cassandra**. Postgres also works at this scale.
For Pastebin: store the **paste content in object storage (S3)** and keep metadata plus the S3 key in the DB.

## 5. High-level design
```
Client → LB → Write API → ID generator → DB (code → long_url)
Client → CDN/LB → Read API → Redis cache → (miss) DB → 302 redirect
                                  └→ async click event → Kafka → analytics store
```

## 6. Deep dives: generating the short code
| Approach | Pros | Cons |
|---|---|---|
| **Hash (MD5/SHA) the URL → take 7 base62 chars** | Same URL → same code (dedup) | Collisions → check and retry with a salt |
| **Counter/ID → base62 encode** | No collisions, short | Sequential = guessable; a single counter is a SPOF → use [Snowflake](05_unique_id_generator.md) or counter ranges per server (via ZooKeeper) |
| **Pre-generated key service (KGS)** | Fast, no collisions | Must track used and unused keys; KGS is its own service |

```python
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62(n):
    s = []
    while n: n, r = divmod(n, 62); s.append(ALPHABET[r])
    return "".join(reversed(s)) or "0"
```

**Caching:** 80/20 rule. Cache the hot 20% of URLs in Redis with LRU eviction. Reads mostly hit the cache.
**Expiration:** lazy deletion on read + a periodic cleanup job.
**Analytics:** never block the redirect. Emit an event to a queue, then aggregate.

## 7. Bottlenecks and tradeoffs
- DB read scaling → cache + read replicas, or shard by `code` (hash).
- Abuse → rate limit link creation ([rate limiter](02_rate_limiter.md)), scan for malicious URLs.
- Custom alias collisions → check uniqueness with a conditional write (`PutItem` with `attribute_not_exists`).

## Follow-ups
- How do you prevent people from enumerating every link? (Random keys, not sequential IDs.)
- Multi-region? (Region-prefixed ID ranges + global DB replication.)

## ✅ Takeaways
Read-heavy → **cache aggressively**. Choosing how to generate IDs is the core decision. Keep analytics async.
