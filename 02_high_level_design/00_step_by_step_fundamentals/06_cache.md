# Step 6 of 13: Cache

[🏠 Overview](README.md) · **← Prev** [Step 5](05_database_replication.md) · **Next →** [Step 7: CDN](07_cdn.md)

## 📍 Where we are
```
User ──▶ LB ──▶ [web servers] ──▶ [primary DB] + [read replicas]
```

## 🚨 The problem
The same data is read **over and over**: the homepage's trending posts, a celebrity's profile, product details. Each read is a database query that takes milliseconds of disk work and connection time. Under heavy traffic, even replicas struggle, and **response times creep up**.

## 💡 The fix: a cache
A cache is a **fast, in-memory key-value store** (Redis, Memcached) that holds the results of expensive operations or frequently read data. Memory is roughly **100× faster than disk**.
```
[web servers] ──1. check──▶ [ CACHE (Redis) ]
      │  hit → return immediately (~1 ms)
      │  miss ↓
      └──2. query──▶ [ DB ] ──3. store result in cache──▶ return
```

## ⚙️ How it works: the cache-aside pattern (most common)
```python
def get_user(user_id):
    user = cache.get(f"user:{user_id}")        # 1. try the cache
    if user is None:                            # 2. miss
        user = db.query("SELECT ... WHERE id=%s", user_id)
        cache.set(f"user:{user_id}", user, ttl=3600)   # 3. populate
    return user

def update_user(user_id, data):
    db.update(user_id, data)
    cache.delete(f"user:{user_id}")             # invalidate; next read refills
```

## 🔀 Decisions you must make (and mention)
| Decision | Guidance |
|---|---|
| **When to use a cache** | Data is **read often, changed rarely**. Never treat the cache as the only copy of important data. |
| **Expiration (TTL)** | Too short → constant DB reloads. Too long → stale data. Add **random jitter** so keys don't all expire at once. |
| **Consistency** | DB and cache can disagree. Delete the cache key on every write (don't update it; that avoids races). |
| **Eviction when full** | **LRU** (least recently used) is the most common; also LFU, FIFO. |
| **Single point of failure** | Run a cache **cluster** with replicas, spread across availability zones. |
| **Sizing** | Use the 80/20 rule: cache the hot 20% of the data, which serves about 80% of reads. |
| Write strategies | Cache-aside (above), write-through (write cache + DB together), write-behind (write cache, flush to DB later: fast but risky) |

## ⚖️ Pitfalls
- **Cache stampede:** a hot key expires and thousands of requests hit the DB at once → use a lock or request coalescing on refill, and staggered TTLs.
- **Hot key:** one key receives huge traffic → replicate it or add a local in-process cache.
- **Penetration:** repeated lookups for non-existent keys → briefly cache "not found" results, or use a Bloom filter.
- Caches add a consistency problem. Don't cache what must be perfectly fresh (an account balance mid-transaction).

## 🗣️ Say it in an interview
> "Redis cache-aside in front of the DB, with a 1-hour TTL plus jitter and delete-on-write invalidation. That should absorb most reads. For hot keys I'd add a short-lived local cache, and I'd lock on refill to prevent stampedes."

## 🔗 Go deeper
- [Caching module](../06_caching/) · runnable [LRU cache](../../03_low_level_design/problems/lru_cache.py) · design problem: [key-value cache](../12_problems/easy/03_key_value_cache.md)
- Primer: [Cache](https://github.com/donnemartin/system-design-primer#cache) · [When to update the cache](https://github.com/donnemartin/system-design-primer#when-to-update-the-cache)

## ✅ Self-check
- [ ] Write cache-aside read and write logic from memory
- [ ] Name 4 decisions you must make when adding a cache
- [ ] What is a cache stampede, and how do you prevent it?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Explain the cache-aside pattern, including how writes are handled.</b></summary>

**Read:** check the cache; on a hit, return it. On a miss, read the DB, write the result to the cache with a TTL, and return it. **Write:** update the DB, then **delete** the cache key so the next read reloads fresh data. The app controls the cache, and a cache outage only degrades performance.

</details>

<details>
<summary><b>Q2. Why delete the cache key on update instead of writing the new value into the cache?</b></summary>

It avoids **race conditions**. Two concurrent updates can write to the DB in one order and to the cache in the other, leaving a stale value cached indefinitely. Deleting is idempotent and simpler: the next reader repopulates the cache from the source of truth.

</details>

<details>
<summary><b>Q3. What is a cache stampede, and how do you prevent it?</b></summary>

A popular key expires and thousands of requests miss at once and hammer the DB. Prevention: a **lock or single-flight** so only one request rebuilds the value while others wait or get stale data, **jittered TTLs**, **refresh-ahead** for hot keys, and serving stale-while-revalidate.

</details>

<details>
<summary><b>Q4. How do you choose the TTL and the eviction policy?</b></summary>

TTL reflects **how stale the data can safely be**: seconds for prices or inventory counts, hours for profiles, days for static reference data. Add jitter. **LRU** eviction is the usual default, since recently used data tends to be used again. LFU suits stable popularity patterns.

</details>

<details>
<summary><b>Q5. What data should NOT be cached?</b></summary>

Data that must be **perfectly fresh and consistent** (account balance during a transaction, seat inventory at the moment of booking), data that's rarely reread (cache pollution), highly personalized one-off results, and sensitive data unless the cache is secured and access-controlled.

</details>

**Next →** [Step 7: CDN](07_cdn.md)
