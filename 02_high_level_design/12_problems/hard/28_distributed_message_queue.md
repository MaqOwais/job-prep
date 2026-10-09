# 🔴 28. Distributed Message Queue (design Kafka)

📖 Related: [Asynchronism & queues](../../07_asynchronism_queues/) · [Kafka design docs](https://kafka.apache.org/documentation/#design) · [Distributed KV store (replication ideas)](17_distributed_kv_store.md)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** producers publish messages to **topics**; consumers read them in **consumer groups** (each group gets every message; within a group each message goes to one consumer); messages are retained for N days and **replayable**; ordering within a partition.
**Non-functional:** very high throughput (millions of msgs/s), low latency, durable (no loss after acknowledgment), horizontally scalable, fault tolerant.

## 2. Core design: a partitioned, replicated append-only log
```
Topic "orders" = partitions P0..Pn, each an ordered, append-only log on disk:
   P0: [m0][m1][m2][m3]…   ← each message has an OFFSET
Producer: partition = hash(key) % n  (same key → same partition → ordered)  | round-robin if no key
Consumer group: partitions are assigned to consumers (one partition → one consumer in the group);
                consumer tracks its OFFSET (committed to an internal topic) → replay = reset offset
```

## 3. High-level design
```
Producers ─▶ Brokers (cluster) ─▶ Consumers (groups)
   each partition has 1 LEADER replica + F FOLLOWERS on other brokers (replication factor 3)
   producer writes to the leader → followers pull & append → ISR (in-sync replicas)
   acks=all → ack after all ISR have it (durable) | acks=1 → leader only (faster, risk loss)
Controller / metadata: KRaft (Raft quorum) or ZooKeeper — partition leadership, broker membership, topic config
Storage per partition: segment files (e.g. 1 GB) + sparse offset index; old segments deleted by retention or compacted by key
```

## 4. Deep dives
- **Why it's fast:** sequential disk writes, OS page cache, **zero-copy** (`sendfile`) from disk to network, batching + compression, consumers pull at their own pace.
- **Durability:** replication factor 3, `acks=all`, `min.insync.replicas=2`. A leader dies → the controller elects a new leader from the ISR (no data loss for committed messages).
- **Delivery semantics:** at-most-once (commit the offset before processing), **at-least-once** (process, then commit; the default), exactly-once (idempotent producer + transactions, where the read-process-write cycle is atomic).
- **Ordering:** only within a partition. More partitions = more parallelism, but a key's order is preserved only within its partition.
- **Consumer rebalancing:** consumers join or leave → partitions get reassigned (cooperative rebalancing minimizes the pause).
- **Retention:** time- or size-based deletion, or **log compaction** (keep the latest value per key, which is useful for changelogs).
- **Back pressure:** consumers pull, so a slow consumer just lags (monitor **consumer lag**) and doesn't block the broker.
- **Kafka vs SQS:** a log with replay and multiple consumer groups vs a queue that deletes messages after acknowledgment, with no replay and simpler ops.

## ✅ Takeaways
**Partitioned, replicated append-only log** with offsets, leader/follower + ISR + acks, consumer groups, zero-copy sequential I/O, and an explanation of the delivery semantics.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How does Kafka guarantee ordering?</b></summary>

Only **within a partition**: messages are appended sequentially with increasing offsets and consumed in order. Producers send related messages (same key) to the same partition via hash(key). There's no global order across partitions.

</details>

<details>
<summary><b>Q2. How does Kafka avoid losing acknowledged messages?</b></summary>

Replication factor 3 with one **leader** and followers. With **acks=all** and **min.insync.replicas=2**, a write is acknowledged only after it's in the in-sync replicas. If the leader fails, a new leader is elected **from the ISR**, so committed data survives.

</details>

<details>
<summary><b>Q3. Why is Kafka so fast?</b></summary>

**Sequential disk I/O** (append-only logs), heavy use of the OS **page cache**, **zero-copy** transfer (sendfile) from disk to socket, producer **batching and compression**, and consumers pulling at their own pace, so the broker keeps no per-message state for consumers.

</details>

<details>
<summary><b>Q4. How do consumer groups work?</b></summary>

Each partition is assigned to **exactly one consumer** in a group, which gives parallelism up to the number of partitions. Different groups each receive all messages independently. Consumers commit **offsets**, and rebalancing reassigns partitions when consumers join or leave.

</details>

<details>
<summary><b>Q5. Kafka vs SQS: when would you use each?</b></summary>

**Kafka:** high-throughput event streaming, **replay**, multiple independent consumer groups, ordered partitions, stream processing. **SQS:** simple fully managed work queues where each message is processed once and deleted, with no replay and minimal operations.

</details>
