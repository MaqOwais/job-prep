# 6. Caching

📖 Primer: [Cache](https://github.com/donnemartin/system-design-primer#cache) · [Client caching](https://github.com/donnemartin/system-design-primer#client-caching) · [CDN caching](https://github.com/donnemartin/system-design-primer#cdn-caching) · [Web server caching](https://github.com/donnemartin/system-design-primer#web-server-caching) · [Database caching](https://github.com/donnemartin/system-design-primer#database-caching) · [Application caching](https://github.com/donnemartin/system-design-primer#application-caching) · [When to update the cache](https://github.com/donnemartin/system-design-primer#when-to-update-the-cache)

---

## 6.1 Where to cache (from the client to the DB)
Client/browser → **CDN** → web server / reverse proxy (Varnish, NGINX) → **application cache (Redis/Memcached)** → database buffer cache.

## 6.2 What to cache
- **Query-level:** hash the query → cache the result. Hard to invalidate when data changes.
- **Object-level (preferred):** cache assembled objects (a user profile, a rendered page fragment, an activity stream). Easy to invalidate when the object changes, and works with async workers.

Good candidates: user sessions, fully rendered pages, activity streams, user graph data, hot items.

## 6.3 Cache update strategies (frequently asked)
| Strategy | How | Pros | Cons |
|---|---|---|---|
| **Cache-aside (lazy loading)** | App reads the cache → on a miss, reads the DB → writes the cache | Only caches what's requested; cache failure isn't fatal | Miss = 3 round trips; stale data until TTL |
| **Write-through** | App writes to the cache → cache writes to the DB synchronously | Cache is always fresh | Slower writes; caches data that may never be read |
| **Write-behind (write-back)** | Write to the cache → asynchronously flush to the DB | Very fast writes | **Data loss** if the cache dies before flushing |
| **Refresh-ahead** | Refresh popular items before they expire | Lower latency | Wasted work if the prediction is wrong |

```python
# Cache-aside
def get_user(uid):
    user = cache.get(f"user:{uid}")
    if user is None:
        user = db.query("SELECT * FROM users WHERE id = %s", uid)
        cache.set(f"user:{uid}", user, ttl=3600)
    return user
# On update: write the DB, then DELETE the cache key (don't update it, to avoid races)
```

## 6.4 Eviction policies
**LRU** (most common; see [LRU cache LLD](../../03_low_level_design/problems/lru_cache.py)), LFU, FIFO, TTL-based, random.

## 6.5 Cache problems and fixes
| Problem | What happens | Fix |
|---|---|---|
| **Cache stampede / thundering herd** | A hot key expires → thousands of requests hit the DB | Mutex/lock on rebuild, request coalescing, staggered/jittered TTLs, refresh-ahead |
| **Cache penetration** | Requests for keys that don't exist always miss | Cache nulls briefly, Bloom filter |
| **Hot key** | One key gets huge traffic → one cache node overloads | Replicate the key (`key#1..N`), local in-process cache |
| **Stale data** | Cache and DB disagree | TTL, delete the key on write, CDC-based invalidation |
| **Cold start** | Empty cache after a deploy or restart | Warm-up scripts |

## 6.6 Redis vs Memcached
| Redis | Memcached |
|---|---|
| Rich data structures (lists, sets, sorted sets, streams, hashes) | Simple strings |
| Persistence, replication, pub/sub, Lua scripts | Pure in-memory, multithreaded |
| Use for leaderboards (sorted sets), rate limiting, queues | Simple large-scale object caching |

## 🗣️ Say it in an interview
> "Cache-aside with Redis, a 1-hour TTL with jitter, and delete-on-write. For hot celebrity profiles I'd add an in-process cache with a 5-second TTL to protect the Redis node."

## ✅ Self-check
- [ ] Compare the 4 update strategies; which loses data?
- [ ] How do you prevent a cache stampede?
- [ ] Why delete the cache key on write instead of updating it?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Compare cache-aside, write-through, and write-behind.</b></summary>

**Cache-aside:** the app loads on a miss and invalidates on write. Simple and resilient, but the first read is slow and data can be stale. **Write-through:** writes go to the cache and the DB synchronously. The cache is always fresh, but writes are slower and cold data gets cached. **Write-behind:** write to the cache and flush to the DB asynchronously. Fastest writes, but **you can lose data** if the cache dies.

</details>

<details>
<summary><b>Q2. Cache penetration vs cache stampede vs hot key: what's the difference?</b></summary>

**Penetration:** requests for keys that don't exist always miss and hit the DB (fix: cache nulls, Bloom filter). **Stampede:** a popular key expires and many requests rebuild it at once (fix: lock/single-flight, jitter, refresh-ahead). **Hot key:** one key gets so much traffic that a single cache node overloads (fix: replicate the key, local cache).

</details>

<details>
<summary><b>Q3. Redis or Memcached?</b></summary>

**Redis**: rich data structures (sorted sets, lists, streams, hashes), persistence, replication, pub/sub, Lua scripts. Use it for leaderboards, rate limiting, and queues. **Memcached**: simple multithreaded string cache, easy to scale for plain object caching. Most new designs choose Redis (or Valkey).

</details>

<details>
<summary><b>Q4. How do you keep the cache consistent with the database?</b></summary>

Make the DB the source of truth. On write, **update the DB then delete the cache key**. Use TTLs as a safety net. For stronger guarantees, invalidate via **CDC** (change data capture from the DB log). Accept bounded staleness, and don't cache data that needs perfect freshness.

</details>

<details>
<summary><b>Q5. How would you size a cache for a system with 100M daily users?</b></summary>

Estimate the **hot working set** (80/20 rule): e.g., 20% of 100M users × 1 KB profile ≈ 20 GB, plus the other hot objects. Add replication overhead and headroom (×1.5–2), then pick node sizes. Validate with the hit rate in production and tune the TTL and memory.

</details>
