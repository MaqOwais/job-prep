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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why bidirectional BFS?</b></summary>

Searching from both users toward each other explores about **b^(d/2) + b^(d/2)** nodes instead of **b^d** (b = average friends, d = distance). With b = 100 and d = 4, that's ~20K vs ~100M nodes.

</details>

<details>
<summary><b>Q2. The graph doesn't fit on one machine. How do you run BFS?</b></summary>

Shard adjacency lists by user ID across person servers. A lookup service maps users to servers. The BFS coordinator expands the frontier in **batches**, grouping user IDs by shard so it makes one RPC per shard per level, and tracks visited nodes and parents itself.

</details>

<details>
<summary><b>Q3. How can you reduce cross-shard calls?</b></summary>

**Locality-aware partitioning**: place friends together (by geography, school, or community detection), so most edges stay inside a shard. Also cache the friend lists of popular users and precompute 2-hop neighborhoods.

</details>

<details>
<summary><b>Q4. How would you compute 'people you may know'?</b></summary>

Count **mutual friends** (friends-of-friends who aren't already friends) and combine it with signals like shared groups, contacts, and location. Precompute offline (batch graph jobs), rank with an ML model, and serve from a cache.

</details>

<details>
<summary><b>Q5. What about users with millions of connections?</b></summary>

Treat **supernodes** specially: skip or sample them during BFS (they connect almost everyone, so they add little information), store their edges separately, and cache aggressively.

</details>
