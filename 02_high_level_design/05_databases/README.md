# 5. Databases

📖 Primer: [Database](https://github.com/donnemartin/system-design-primer#database) · [RDBMS](https://github.com/donnemartin/system-design-primer#relational-database-management-system-rdbms) · [Master-slave replication](https://github.com/donnemartin/system-design-primer#master-slave-replication) · [Master-master replication](https://github.com/donnemartin/system-design-primer#master-master-replication) · [Federation](https://github.com/donnemartin/system-design-primer#federation) · [Sharding](https://github.com/donnemartin/system-design-primer#sharding) · [Denormalization](https://github.com/donnemartin/system-design-primer#denormalization) · [SQL tuning](https://github.com/donnemartin/system-design-primer#sql-tuning) · [NoSQL](https://github.com/donnemartin/system-design-primer#nosql) · [SQL or NoSQL](https://github.com/donnemartin/system-design-primer#sql-or-nosql)

---

## 5.1 Relational databases (RDBMS) and ACID
- **A**tomicity: all or nothing · **C**onsistency: constraints always hold · **I**solation: concurrent transactions don't interfere · **D**urability: committed means saved.
- Isolation levels: Read Uncommitted → Read Committed → Repeatable Read → Serializable (each prevents dirty reads, then non-repeatable reads, then phantom reads).
- Indexes: **B-tree** (range queries) or hash (exact match). Indexes speed up reads but slow down writes and use space.

## 5.2 Scaling a relational database (in roughly this order)
| Technique | What | Tradeoff |
|---|---|---|
| **Vertical scale + indexes + query tuning** | Do this first | Hits a ceiling eventually |
| **Caching** | Redis in front of the DB | Invalidation complexity |
| **Master-slave (primary-replica) replication** | Writes go to the primary; reads go to replicas | **Replication lag** (stale reads); failover logic |
| **Master-master replication** | Both nodes accept writes | Conflict resolution, loose consistency or higher write latency |
| **Federation** (functional partitioning) | Separate DBs by function: users DB, products DB, forums DB | Cross-DB joins happen in app code |
| **Sharding** (horizontal partitioning) | Split rows across DBs by a shard key | Hot shards, re-sharding, cross-shard queries and transactions |
| **Denormalization** | Duplicate data to avoid joins | Writes are more complex; possible inconsistency |

### Sharding: what interviewers ask
- **Shard key choice:** high cardinality, even distribution, matches the main query (e.g. `user_id`).
- **Strategies:** range-based (easy range queries, risk of hot spots), hash-based (even distribution, no range queries), **consistent hashing** (easy rebalancing), directory/lookup service (flexible, but an extra hop and a possible SPOF).
- **Problems:** celebrity/hot keys, joins across shards, global secondary indexes, resharding.

### Replication: what interviewers ask
- **Synchronous** (no data loss, slower writes) vs **asynchronous** (fast, possible loss on failover).
- **Read-your-writes:** route a user's reads to the primary for a few seconds after they write.
- **Leader election:** Raft or Paxos (ZooKeeper, etcd).

## 5.3 SQL tuning checklist
Benchmark and profile (`EXPLAIN`, slow query log) → add the right indexes → avoid `SELECT *` → use `CHAR` for fixed-length fields and `TEXT` for large blobs (or move blobs to object storage) → avoid expensive joins (denormalize where it helps) → partition tables → tune the query cache or connection pool.

## 5.4 NoSQL families
| Type | Model | Examples | Use for |
|---|---|---|---|
| **Key-value** | `key → value`, O(1) | Redis, DynamoDB, Memcached | Sessions, caching, carts, rate limits |
| **Document** | JSON documents, flexible schema | MongoDB, DynamoDB, Couchbase | Catalogs, user profiles, CMS |
| **Wide-column** | Row key → column families; LSM-tree storage | Cassandra, HBase, Bigtable | **Write-heavy**, time-series, messages, feeds |
| **Graph** | Nodes + edges | Neo4j, Neptune | Social graphs, recommendations, fraud |
| Search | Inverted index | Elasticsearch, OpenSearch | Full-text search, logs |
| Time-series | Time-ordered | InfluxDB, Timestream | Metrics, IoT |
| Vector | Embeddings, ANN search | pgvector, Pinecone, OpenSearch | RAG, semantic search |

**BASE:** Basically Available, Soft state, Eventual consistency.
**LSM tree vs B-tree:** an LSM tree appends writes to a memtable, flushes them to SSTables, and compacts later, so writes are fast. A B-tree updates data in place, so reads are fast.

## 5.5 SQL or NoSQL?
| Choose SQL when… | Choose NoSQL when… |
|---|---|
| Structured data, relationships, joins | Semi-structured data, flexible schema |
| Transactions / strong consistency (payments, inventory) | Massive scale, very high write throughput |
| Complex ad-hoc queries | Simple, known access patterns (key lookups) |
| Data fits on one node (or a few) | Need horizontal scale, multi-region |

> **Interview tip:** saying "it depends on the access patterns" isn't enough. Name the access pattern and **then** pick a database.

## 🗣️ Say it in an interview
> "Messages are write-heavy and read by conversation in time order, so I'd use Cassandra with partition key `conversation_id` and clustering key `message_id` (time-sortable). User accounts and billing go in Postgres for transactions."

## ✅ Self-check
- [ ] Replica vs sharding: what problem does each solve?
- [ ] Pick a shard key for Twitter tweets and explain the hot-key problem
- [ ] Explain LSM tree vs B-tree in 30 seconds
- [ ] SQL vs NoSQL for 3 different features of one app

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What are the isolation levels, and which anomaly does each prevent?</b></summary>

**Read uncommitted** → nothing. **Read committed** → dirty reads. **Repeatable read** → non-repeatable reads too. **Serializable** → phantoms too (transactions behave as if run one at a time). Higher isolation means more locking or aborts, so most apps use read committed plus targeted locking.

</details>

<details>
<summary><b>Q2. Federation vs sharding: what's the difference?</b></summary>

**Federation** (functional partitioning) splits databases **by feature**: users DB, products DB, orders DB. **Sharding** splits **one table's rows** across many DBs by a key. Federation is simpler but limited by the biggest feature. Sharding scales a single huge dataset.

</details>

<details>
<summary><b>Q3. Why do write-heavy systems often use LSM-tree databases like Cassandra?</b></summary>

LSM trees turn random writes into **sequential appends** (commit log + memtable, flushed to immutable SSTables), so writes are very fast. Reads may check several SSTables, which Bloom filters and compaction mitigate. B-trees update pages in place, which favors reads.

</details>

<details>
<summary><b>Q4. What is denormalization, and when is it worth it?</b></summary>

Storing **redundant copies** of data (e.g., the author's name inside each post) to avoid joins. It's worth it for read-heavy paths, sharded data where joins cross shards, and precomputed views. The cost: more complex writes, and copies can drift (fix them with async updates or CDC).

</details>

<details>
<summary><b>Q5. How would you pick a database for a new feature?</b></summary>

Start from **access patterns and requirements**: query shapes (key lookups, ranges, joins, search, graph), read/write ratio, consistency needs, scale, and latency. Then choose: relational for transactions and joins, KV/wide-column for huge simple-access scale, document for flexible schemas, search engine for text, graph for relationships, TSDB for metrics.

</details>
