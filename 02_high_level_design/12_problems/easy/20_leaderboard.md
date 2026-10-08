# 🟢 20. Real-Time Leaderboard (gaming / top-K)

📖 Related: [Caching: Redis vs Memcached](../../06_caching/) · coding [Heaps / top-k](../../../01_coding/09_heap_priority_queue/) · [Redis sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
⏱️ Try it yourself first: 30 minutes.

## 1. Requirements
**Functional:** update a player's score after each game; show the **top 10 globally**; show **my rank** and the players around me; monthly leaderboards (reset each month).
**Non-functional:** real-time (a rank updates within a second), 25M monthly active users, 5K score updates/s at peak, reads ≫ writes.

## 2. Key data structure: the Redis sorted set
```
ZINCRBY leaderboard:2026-10 <points> <user_id>     # O(log n) update
ZREVRANGE leaderboard:2026-10 0 9 WITHSCORES       # top 10, O(log n + 10)
ZREVRANK  leaderboard:2026-10 <user_id>            # my rank, O(log n)
ZREVRANGE leaderboard:2026-10 (rank-4) (rank+4)    # neighbors
```
A sorted set is a skip list + a hashmap, so every operation is O(log n). 25M members × ~100 B ≈ **2.5 GB**, which fits on one Redis node (with replicas for HA and read scaling).

## 3. High-level design
```
Game servers → (authenticated, server-side scoring!) → Score service
      → 1. write score event to DB (source of truth: scores(user_id, game_id, points, ts)) / Kafka
      → 2. ZINCRBY in Redis
Clients → Leaderboard API → Redis (top 10 cached for ~1s; my rank) → hydrate names/avatars from user cache
Monthly reset: new key per month (leaderboard:YYYY-MM); old keys expire or are archived
```

## 4. Deep dives
- **Never trust the client:** game servers compute scores. This prevents cheating.
- **Durability:** Redis is fast but isn't the source of truth. Rebuild the sorted set from the DB or Kafka after a failure (plus Redis AOF persistence and replicas).
- **Scaling beyond one node** (e.g., 500M users):
  - Shard by **score range** (each shard holds a band of scores; the top 10 is in the top shard; your rank = your rank within your shard + the counts of all higher shards). Rebalancing is needed as scores shift.
  - Or shard by user hash and **scatter-gather the top 10 from each shard** and merge them (easy for top-K, hard for an exact global rank).
  - Approximate ranks ("top 5%") at very large scale are usually acceptable.
- **Ties:** compose the score as `points * 1e10 + (MAX_TS - timestamp)` so the earlier achiever ranks higher.
- **Alternative:** a relational DB with an index on score works at small scale. `ORDER BY score LIMIT 10` is fine, but computing *my rank* requires `COUNT(*) WHERE score > mine`, which is slow at scale.

## ✅ Takeaways
**Redis sorted sets** (ZINCRBY, ZREVRANGE, ZREVRANK), DB/Kafka as the source of truth, server-side scoring, and sharding by score range for huge scale.
