# 🔴 29. Stock Exchange / Order Matching Engine

📖 Related: coding [Heaps](../../../01_coding/09_heap_priority_queue/) · [LMAX architecture (Martin Fowler)](https://martinfowler.com/articles/lmax.html)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** place and cancel limit and market orders; match buy and sell orders (price-time priority); publish trades and market data (order book depth, last price); risk checks (enough balance or shares).
**Non-functional:** **ultra-low latency** (microseconds to milliseconds), very high throughput, **deterministic and fair** (same input → same output), never lose an order, a full audit trail.

## 2. The order book (the core data structure)
Per symbol: **bids** (buy orders, highest price first) and **asks** (sell orders, lowest price first). At each price level, a FIFO queue of orders.
```
ASKS  101.02: [s7 50]                 Incoming BUY 120 @ 101.01 →
      101.01: [s3 100] [s5 30]          fills s3 100 @101.01, s5 20 @101.01 (time priority)
------------------------------          s5 left with 10
BIDS  100.99: [b2 200]                Remaining 0 → done. Trades published.
      100.98: [b4 10] [b9 75]
```
Implementation: price levels in a sorted map / two [heaps](../../../01_coding/09_heap_priority_queue/) + a doubly linked list per level + a hashmap `order_id → node` for **O(1) cancel**.

## 3. High-level design
```
Brokers/clients → Gateway (FIX/binary protocol, auth, rate limit, validation)
   → Risk check (pre-trade: balance/position, limits — in-memory)
   → SEQUENCER: assigns a global, monotonically increasing sequence number to every inbound event
        and writes it to a replicated, append-only EVENT LOG (journal) → determinism + recovery
   → MATCHING ENGINE (single-threaded per symbol shard, all in memory, no locks): apply event → trades/updates
   → outbound sequencer → Market data publisher (multicast/WebSocket: depth, trades)
                         → Execution reports to clients
                         → Post-trade: clearing/settlement, ledger DB, reporting (async)
Hot standby engine replays the same log → identical state → fast failover
```

## 4. Deep dives
- **Why single-threaded?** No locks or contention gives deterministic, very fast processing (the LMAX pattern). Scale by **sharding symbols** across engines.
- **Event sourcing:** the input log *is* the source of truth. State = replay(log). Recovery and the hot standby come from replay. Snapshots speed up restarts.
- **Latency techniques:** keep everything in memory, avoid GC pauses (object pools, or C++/Rust), kernel bypass networking, colocation, preallocated ring buffers (the Disruptor pattern).
- **Fairness:** sequencing at the gateway determines time priority; equal network paths for participants.
- **Market data fan-out:** multicast for colocated clients, aggregated snapshots for retail clients.
- **Risk and safety:** circuit breakers (halt trading on extreme moves), fat-finger checks, self-trade prevention.

## ✅ Takeaways
**Order book (price levels + FIFO + O(1) cancel)**, a **sequencer + event log** for determinism, a single-threaded in-memory matching engine per symbol shard, a hot standby by replay.
