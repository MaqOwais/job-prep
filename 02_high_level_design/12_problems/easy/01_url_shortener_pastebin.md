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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do you generate short codes without collisions?</b></summary>

Options: (1) a **unique counter/ID → base62** (no collisions; use Snowflake IDs or per-server ID ranges so there's no central bottleneck), (2) **hash the URL** and take 7 characters, then check for a collision and retry with a salt, (3) a **pre-generated key service**. Counter + base62 is simplest; add randomization if codes must not be guessable.

</details>

<details>
<summary><b>Q2. 301 or 302 redirect?</b></summary>

**301 (permanent)** is cached by browsers, which means less server load but you **lose click analytics** and can't change the target. **302 (temporary)** sends every click through your servers, so you keep analytics and control. Most shorteners use 302 (or 307).

</details>

<details>
<summary><b>Q3. How many characters do you need for the short code?</b></summary>

With base62, 62^6 ≈ 57B and 62^7 ≈ 3.5T combinations. For ~12B URLs over 10 years, **7 characters** gives plenty of headroom.

</details>

<details>
<summary><b>Q4. How do you scale the redirect path to 100K requests per second?</b></summary>

It's read-heavy and the data is immutable: a **Redis cache** (hot 20% of codes), **CDN/edge** caching of redirects, read replicas or a KV store (DynamoDB) partitioned by code, stateless redirect servers behind a load balancer. Analytics go asynchronously to a queue.

</details>

<details>
<summary><b>Q5. How would you implement link expiration and custom aliases?</b></summary>

Store expire_at. Check it on read (**lazy expiry**) and run a periodic cleanup job; optionally use a DB TTL feature. Custom alias: a **conditional insert** (insert only if the key doesn't exist) so two users can't claim the same alias; reserve offensive or system words.

</details>
