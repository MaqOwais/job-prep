# 🟡 10. Typeahead / Search Autocomplete

📖 Related: coding [Tries](../../../01_coding/08_tries/) · [Search Suggestions System (LC 1268)](https://leetcode.com/problems/search-suggestions-system/)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** as the user types, return the **top 5 suggestions** for the prefix, ranked by popularity (and possibly personalization or freshness).
**Non-functional:** **< 100 ms** end to end (the user is typing), highly available, suggestions can be slightly stale (updated hourly or daily).

## 2. Estimates
10M daily active users × 10 searches × ~20 keystrokes = 2B requests/day → ~24K QPS (peak ~50K).

## 3. High-level design
```
Query path:
 Client (debounce 100–200 ms, local cache) → CDN/edge cache → LB → Suggest service
       → Trie cache (in memory, sharded by prefix) → top-5 list stored at each node

Data path (offline):
 Search logs → Kafka → aggregator (Spark/Flink: counts per query, time-decayed)
       → Trie builder (weekly full rebuild + hourly deltas) → Trie DB/snapshot → load into servers
```

## 4. Deep dives
- **Trie with top-k at every node:** lookup is O(prefix length). Instead of traversing the whole subtree, **precompute the top 5** at each node. That uses memory but makes reads O(1) after the walk.
- **Sharding:** by first character(s), adjusted for skew ("s" is far more common than "x"), using a shard map.
- **Updates:** don't update the trie live on every search. Aggregate offline and swap in new trie snapshots (blue/green).
- **Caching:** browser cache (same prefix), CDN for popular prefixes, client debounce.
- **Filtering:** remove offensive or illegal suggestions with a blocklist layer.
- **Personalization / trending:** merge global top-k with the user's recent searches, plus a real-time trending stream (Flink) for news.
- **Alternatives:** Elasticsearch completion suggester, Redis sorted sets per prefix.

## ✅ Takeaways
Trie with **precomputed top-k per node**, an offline aggregation pipeline, aggressive caching and debouncing, and prefix sharding with skew handling.
