# 🟡 11. Social Network Graph: Shortest Path Between Users

📖 Primer solution: [Design the data structures for a social network](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** find the shortest friend path between two users ("You → Alice → Bob"), mutual friends, people you may know.
**Non-functional:** 100M users, 50 friends on average, low latency, and the graph **doesn't fit on one machine**.

## 2. Core algorithm
**BFS** for the shortest path in an unweighted graph (see [coding: graphs](../../../01_coding/11_graphs/)). **Bidirectional BFS** (searching from both ends) cuts the explored nodes dramatically: O(b^(d/2)) vs O(b^d).

## 3. Distributed design
```
Client → LB → Search API → User Graph service
                              │  BFS loop: for each frontier user →
                              ▼
                     Lookup service (user_id → person server)
                              ▼
                     Person servers (sharded by user_id; adjacency lists in memory/DB)
```
- Each BFS step = **batched lookups** of friend lists, grouped by shard (one RPC per shard, not per user).
- Keep a visited set and a parent map in the graph service.

## 4. Deep dives
- **Sharding the graph:** hash by user_id (simple), or **locality-aware partitioning** (friends tend to live in the same country or school → fewer cross-shard hops).
- **Optimizations:** bidirectional BFS, depth limit (6 degrees), caching friend lists of popular users, precomputing 2-hop neighborhoods for "people you may know".
- **Storage options:** adjacency lists in a KV store/Redis; a graph DB (Neo4j, Neptune) for richer queries; [Facebook TAO](https://www.usenix.org/conference/atc13/technical-sessions/presentation/bronson) for very large scale.
- **Celebrity nodes** (millions of edges): skip or sample them during BFS.

## ✅ Takeaways
Bidirectional BFS + sharded adjacency lists + **batching lookups per shard** + caching the friend lists of hot users.
