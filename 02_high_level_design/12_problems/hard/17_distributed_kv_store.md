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
