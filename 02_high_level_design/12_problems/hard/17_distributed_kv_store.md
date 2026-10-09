# 🔴 17. Distributed Key-Value Store (Dynamo / Cassandra)

📖 Related: [Amazon Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) · primer [CAP](https://github.com/donnemartin/system-design-primer#cap-theorem) · [NoSQL](https://github.com/donnemartin/system-design-primer#nosql) · *Designing Data-Intensive Applications*, ch. 5–6
⏱️ Try it yourself first: 45 minutes. **Very common at Amazon.**

## 1. Requirements
`put(key, value)`, `get(key)`. Small values (< 10 KB). Highly available (always writable), horizontally scalable, tunable consistency, automatic failure handling.

## 2. Building blocks (each one answers a question)
| Question | Technique |
|---|---|
| How do we split data across nodes? | **Consistent hashing** + virtual nodes |
| How do we survive node failures? | **Replicate to N nodes** (the next N on the ring = preference list) |
| How do we tune consistency? | **Quorum: W + R > N** (e.g. N=3, W=2, R=2) |
| What about concurrent conflicting writes? | **Vector clocks** (or last-write-wins with timestamps) + read repair |
| A node is temporarily down? | **Sloppy quorum + hinted handoff** |
| Replicas drifted apart? | **Anti-entropy with Merkle trees** |
| Who's alive? | **Gossip protocol** + failure detection |
| How is data stored on each node? | **LSM tree:** commit log → memtable → SSTables + Bloom filters + compaction |

## 3. Architecture
```
Client → any node (coordinator) → hash(key) → preference list [A, B, C]
   write: send to all N, success when W ACKs (others async)
   read:  ask R replicas, return newest; if versions differ → read repair
Node internals: commit log (durability) → memtable (memory) → flush → SSTables (disk)
                Bloom filter per SSTable skips files on reads; compaction merges SSTables
```

## 4. Deep dives
- **Tuning:** W=1 → fast writes, weaker consistency. R=1 → fast reads. W=N → slow but strongly durable writes. `W + R > N` → reads see the latest write (in the absence of sloppy quorum).
- **Conflict resolution:** vector clocks detect concurrent versions → return both to the client (like Dynamo's shopping cart merge), or use LWW (simpler, but can lose data).
- **Write path:** append to the commit log (sequential, fast) → memtable → acknowledge.
- **Read path:** memtable → Bloom filters → SSTables (newest first) → merge.
- **Deletes:** tombstones, removed during compaction after a grace period.
- **Adding nodes:** only the neighbors' key ranges move (consistent hashing).

## ✅ Takeaways
Name all 8 building blocks and the problem each solves. Explain quorum math with N=3. This is the Dynamo paper in one page.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Explain quorum reads and writes with N=3.</b></summary>

Each key is replicated to **N = 3** nodes. A write succeeds after **W** acks and a read queries **R** replicas. If **W + R > N** (e.g., W=2, R=2), read and write sets overlap in at least one node, so reads see the latest acknowledged write. W=1/R=1 is faster but weaker.

</details>

<details>
<summary><b>Q2. What are vector clocks for?</b></summary>

Detecting whether two versions of a value are **causally ordered or concurrent**. Each version carries (node, counter) pairs. If neither clock dominates the other, the versions **conflict** and must be merged (by the app, as with Dynamo's cart) instead of one silently overwriting the other.

</details>

<details>
<summary><b>Q3. What are sloppy quorum and hinted handoff?</b></summary>

If a replica is down, the write goes to the **next healthy node** on the ring (sloppy quorum), which stores a **hint**. When the original node recovers, the hint is handed back. This keeps writes available during failures.

</details>

<details>
<summary><b>Q4. How do replicas that drifted apart get repaired?</b></summary>

**Read repair** (fix stale replicas noticed during reads) and **anti-entropy** using **Merkle trees**: replicas compare tree hashes per key range and sync only the ranges that differ. Efficient even for huge datasets.

</details>

<details>
<summary><b>Q5. Describe the write and read path on a single node.</b></summary>

**Write:** append to the commit log (durability) → insert into the memtable → acknowledge. Memtables flush to immutable **SSTables**, and compaction merges them. **Read:** memtable → SSTables newest first, skipping files via **Bloom filters**, then merge versions. Deletes are tombstones.

</details>
