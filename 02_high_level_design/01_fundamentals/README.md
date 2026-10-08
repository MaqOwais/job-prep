# 1. Fundamentals

📖 Primer: [Performance vs scalability](https://github.com/donnemartin/system-design-primer#performance-vs-scalability) · [Latency vs throughput](https://github.com/donnemartin/system-design-primer#latency-vs-throughput) · [Availability vs consistency](https://github.com/donnemartin/system-design-primer#availability-vs-consistency) · [CAP theorem](https://github.com/donnemartin/system-design-primer#cap-theorem) · [Consistency patterns](https://github.com/donnemartin/system-design-primer#consistency-patterns) · [Availability patterns](https://github.com/donnemartin/system-design-primer#availability-patterns)

---

## 1.1 Performance vs scalability
- **Performance problem:** the system is slow for **one** user.
- **Scalability problem:** the system is fast for one user but slow **under load**.
- A service is **scalable** if adding resources increases performance proportionally.

**Vertical scaling** (a bigger machine): simple, but has a hard ceiling and is a single point of failure.
**Horizontal scaling** (more machines): no ceiling, but needs **stateless** services, load balancing, and distributed data.

## 1.2 Latency vs throughput
- **Latency:** time to do one action (ms).
- **Throughput:** actions per unit of time (QPS/RPS).
- Aim for **maximal throughput with acceptable latency**. Talk about **p50/p95/p99** latency, not averages.

## 1.3 CAP theorem
In a distributed system, during a network **P**artition you must choose:
- **CP (consistency + partition tolerance):** return an error or time out rather than stale data. Use for **banking, inventory counts, locks**. Examples: HBase, ZooKeeper, etcd, MongoDB (default config).
- **AP (availability + partition tolerance):** always respond, possibly with stale data, and converge later. Use for **social feeds, likes, shopping carts, DNS**. Examples: Cassandra, DynamoDB (default), CouchDB.

> Networks aren't reliable, so P isn't optional. The real choice is **C vs A when a partition happens**.
> **PACELC** extends this: *if* Partition → A or C; **E**lse → **L**atency or **C**onsistency.

## 1.4 Consistency patterns
| Pattern | Meaning | Example |
|---|---|---|
| **Weak** | A read after a write may or may not see it | Memcached, VoIP, multiplayer games |
| **Eventual** | Reads *will* see the write eventually (ms–s) | DNS, email, DynamoDB default, S3 replication |
| **Strong** | Reads see the write immediately | RDBMS, file systems, transactions |

Other terms worth knowing: **read-your-writes**, **monotonic reads**, **linearizability**, **quorum** (`W + R > N` ⇒ strong reads).

## 1.5 Availability patterns
**Fail-over**
- **Active-passive:** heartbeats between active and standby; the passive node takes over the IP. Downtime depends on whether the standby is hot or cold.
- **Active-active:** both nodes serve traffic, behind DNS or a load balancer.
- Downsides: more hardware and complexity, and possible data loss if the active node fails before replication.

**Replication:** master-slave and master-master (see [Databases](../05_databases/)).

**Availability in numbers**
| Availability | Downtime/year | Downtime/month |
|---|---|---|
| 99% (two 9s) | 3.65 days | 7.3 h |
| 99.9% (three 9s) | 8.77 h | 43.8 min |
| 99.99% (four 9s) | 52.6 min | 4.38 min |
| 99.999% (five 9s) | 5.26 min | 26 s |

- Components **in sequence:** `A = A1 × A2` → lower overall (0.999 × 0.999 = 0.998).
- Components **in parallel:** `A = 1 − (1−A1)(1−A2)` → higher overall (two 99.9% nodes → 99.9999%).

## 1.6 Other must-know terms
- **SPOF** (single point of failure), **redundancy**, **graceful degradation**
- **Idempotency:** repeating a request has the same effect as doing it once
- **Backpressure**, **circuit breaker**, **retry with exponential backoff + jitter**
- **Stateless vs stateful** services: move session state to Redis or a DB
- **SLA / SLO / SLI:** contract / target / measurement

## 🗣️ Say it in an interview
> "For the timeline I'd choose availability over strong consistency. A user seeing a tweet a second late is fine, but the timeline being down isn't. For the payment ledger I'd choose consistency: CP storage with transactions."

## ✅ Self-check
- [ ] Explain CAP with one AP and one CP example
- [ ] Calculate availability for 2 services in series and in parallel
- [ ] Explain active-passive vs active-active failover
- [ ] Explain why p99 latency matters more than the average
