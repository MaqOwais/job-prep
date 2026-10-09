# Step 12 of 13: Database Sharding (scaling the data tier horizontally)

[🏠 Overview](README.md) · **← Prev** [Step 11](11_logging_metrics_automation.md) · **Next →** [Step 13: Putting it together](13_putting_it_together.md)

## 📍 Where we are
Caches and read replicas handle reads well. But now we have **500M users** and heavy **writes**.

## 🚨 The problem
- Every write still goes to **one primary**. It's at its limit (CPU, disk I/O, connections).
- The dataset (tens of TB) **doesn't fit** on one machine, and indexes no longer fit in memory, so queries slow down.
- Vertical scaling (a bigger DB machine) is maxed out or absurdly expensive.

## 💡 The fix: sharding (horizontal partitioning)
Split **one big database into many smaller ones (shards)**. Each shard has the **same schema** but holds a **different subset of rows**. Each shard is its own primary + replicas.
```
                         shard = hash(user_id) % 4
[app] ──┬──▶ Shard 0: users whose hash%4 = 0   (primary + replicas)
        ├──▶ Shard 1: users whose hash%4 = 1
        ├──▶ Shard 2: users whose hash%4 = 2
        └──▶ Shard 3: users whose hash%4 = 3
```
Writes and storage are now spread across 4 machines (or 400).

## ⚙️ The sharding key (the most important decision)
The **shard (partition) key** decides which shard a row lives on. A good key:
- Has **high cardinality** and spreads data and traffic **evenly**.
- Matches the **main query pattern**, so most queries hit **one** shard (e.g., `user_id` when you mostly query "this user's data").

| Strategy | How | Pros | Cons |
|---|---|---|---|
| **Hash-based** | `hash(key) % N` | Even distribution | Range queries span all shards; changing N moves most data |
| **Consistent hashing** | Hash ring + virtual nodes | Adding a shard moves only ~1/N of the data | A bit more complex |
| **Range-based** | user_id 1–1M → shard A, … | Range scans are easy | **Hot spots** (new users all land on the last shard) |
| **Directory / lookup table** | A service maps key → shard | Flexible, easy to move tenants | An extra lookup; the directory must be highly available |
| Geo-based | Region → shard | Data residency, locality | Uneven region sizes |

## ⚖️ The problems sharding brings (always mention these)
1. **Resharding:** a shard fills up or grows uneven → split it and move data. Consistent hashing or a directory makes this less painful. Plan for it.
2. **Celebrity / hot-key problem:** one shard gets a huge share of traffic (Justin Bieber's posts) → give hot entities dedicated shards, or split their keys further.
3. **Joins and cross-shard queries:** you can't JOIN across shards easily → **denormalize** (duplicate data so queries stay on one shard) or do the join in the app, or with scatter-gather queries.
4. **Cross-shard transactions** are hard (2-phase commit or sagas). Design so transactions stay within one shard.
5. Global unique IDs: auto-increment per shard collides → use [Snowflake IDs](../12_problems/easy/05_unique_id_generator.md).

> **Shard last, not first.** Exhaust indexes, query tuning, caching, read replicas, vertical scaling, and moving some data to NoSQL first. Some databases shard for you (DynamoDB, Cassandra, Vitess for MySQL, Citus for Postgres, Aurora Limitless).

## 🗣️ Say it in an interview
> "Once writes outgrow one primary, I'd shard by user_id using consistent hashing, so a user's data lives on one shard and resharding moves little data. I'd denormalize to avoid cross-shard joins, use Snowflake IDs, and handle celebrity accounts with dedicated shards."

## 🔗 Go deeper
- [Databases module: sharding, federation, denormalization](../05_databases/) · [Consistent hashing](../03_load_balancing_reverse_proxy/) · [Distributed KV store problem](../12_problems/hard/17_distributed_kv_store.md)
- Primer: [Sharding](https://github.com/donnemartin/system-design-primer#sharding) · [Federation](https://github.com/donnemartin/system-design-primer#federation) · [Denormalization](https://github.com/donnemartin/system-design-primer#denormalization)

## ✅ Self-check
- [ ] Replication vs sharding: which one scales writes?
- [ ] What makes a good shard key? Pick one for Twitter and justify it
- [ ] List the 4 big problems sharding introduces, with a fix for each
- [ ] Why does consistent hashing make resharding easier?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Replication vs sharding: what does each solve?</b></summary>

**Replication** copies the same data to multiple machines. It scales **reads** and provides availability. **Sharding** splits different data across machines. It scales **writes and storage**. Large systems use both: each shard is a primary with its own replicas.

</details>

<details>
<summary><b>Q2. What makes a good shard key? Pick one for a chat app.</b></summary>

High cardinality, an **even distribution** of data and traffic, and it matches the main access pattern so most queries hit **one shard**. For chat: **conversation_id**, since messages are read and written per conversation (bucketed by time for very large group chats).

</details>

<details>
<summary><b>Q3. What is the celebrity (hot key) problem, and how do you handle it?</b></summary>

One key gets a huge share of traffic (a celebrity's posts or profile), overloading its shard. Fixes: give hot entities **dedicated shards**, **split the key** (key#1..N) and aggregate across the pieces, cache aggressively, and handle these entities specially (e.g., fan-out on read).

</details>

<details>
<summary><b>Q4. How does consistent hashing help with resharding?</b></summary>

With hash % N, changing N remaps almost **every** key. With consistent hashing, keys and nodes sit on a ring, and adding or removing a node moves only the keys in **one neighboring segment (~1/N)**. Virtual nodes even out the distribution.

</details>

<details>
<summary><b>Q5. What do you lose when you shard, and how do you compensate?</b></summary>

**Cross-shard joins** (denormalize, or join in the application), **cross-shard transactions** (keep transactions within a shard, or use sagas/2PC), **global uniqueness** (Snowflake IDs), **simple global queries** (scatter-gather, or a separate analytics store), plus the operational cost of rebalancing.

</details>

**Next →** [Step 13: Putting it all together](13_putting_it_together.md)
