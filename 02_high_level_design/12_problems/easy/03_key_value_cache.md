# 🟢 03. Key-Value Cache for a Search Engine's Query Results

📖 Primer solution: [Design a key-value cache to save the results of the most recent web server queries](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** cache the results of recent search queries. On a hit, return the cached results. On a miss, query the backend and cache the result. Evict entries when full or expired.
**Non-functional:** low latency, high availability, and a hot set that exceeds a single machine's memory.

## 2. Estimates (from the primer)
- 10M users, 10B queries/month → ~4,000 QPS.
- Each entry: query (~50 B) + title (~20 B) + snippet (~200 B) ≈ 270 B.
- If every query were unique: 2.7 TB/month. **Memory is limited**, so you need eviction (LRU).

## 3. Core design
```
Client → Web server (reverse proxy) → Query API → Memory cache (LRU)
                                                   │ miss
                                                   ▼
                                       Reverse index service + Document service
```
**LRU = hashmap + doubly linked list**, O(1) get and put. See the runnable [LRU cache](../../../03_low_level_design/problems/lru_cache.py).

## 4. Deep dives
**When to update the cache:**
- TTL on every entry (search results go stale), plus explicit invalidation when a page's content changes.

**Scaling beyond one machine:**
| Option | Notes |
|---|---|
| Each server has its own cache | Simple, but a low hit rate and duplicated entries |
| Copy of the whole cache on every server | Simple reads, but wastes memory |
| **Shard the cache: `hash(query) % N`** | Better, but resizing remaps every key |
| **Consistent hashing** ✓ | Adding or removing a node remaps only ~1/N of the keys |

**Normalization:** lowercase, trim, sort the query terms before hashing, which raises the hit rate.
**Memcached vs Redis:** both work. Redis adds persistence and replication.
**Hot keys:** replicate trending queries, or add a local L1 cache.
**Cache stampede:** lock or coalesce requests when a hot key expires.

## ✅ Takeaways
LRU implementation + TTL + consistent-hashing sharding + query normalization. This problem often turns into "now code the LRU", so be ready to write it in 10 minutes.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why is LRU implemented with a hash map plus a doubly linked list?</b></summary>

The **hash map** gives O(1) lookup of a key's node. The **doubly linked list** keeps recency order and lets you move a node to the front or remove the tail in **O(1)** (you have the prev/next pointers). Together, get and put are both O(1).

</details>

<details>
<summary><b>Q2. How do you scale the cache beyond one machine?</b></summary>

**Shard** keys across nodes with **consistent hashing** (+ virtual nodes), so adding or removing nodes moves only ~1/N of the keys. Add replicas per shard for availability. Clients or a proxy layer (twemproxy, a Redis Cluster-aware client) route keys to nodes.

</details>

<details>
<summary><b>Q3. How do you keep cached search results fresh?</b></summary>

A **TTL** on every entry (results go stale as the index changes), plus explicit invalidation when important documents change. Accept some staleness for search, since users tolerate results a few minutes old.

</details>

<details>
<summary><b>Q4. How do you increase the cache hit rate for search queries?</b></summary>

**Normalize queries** before hashing (lowercase, trim, collapse whitespace, sort terms if the order doesn't matter), cache popular queries longer, pre-warm trending queries, and size the cache for the hot working set.

</details>

<details>
<summary><b>Q5. What happens when a cache node fails?</b></summary>

Its keys miss and fall through to the backend, which causes a load spike. Mitigate with replicas per shard and automatic failover, consistent hashing (only that node's keys are affected), and request coalescing to protect the backend while the cache warms up again.

</details>
