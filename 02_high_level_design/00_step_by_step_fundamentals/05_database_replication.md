# Step 5 of 13: Database Replication

[🏠 Overview](README.md) · **← Prev** [Step 4](04_load_balancer.md) · **Next →** [Step 6: Cache](06_cache.md)

## 📍 Where we are
```
User ──▶ LB ──▶ [web 1][web 2][web 3] ──▶ [ ONE database ]
```
The web tier is now redundant and scalable. The database isn't.

## 🚨 The problem
- **Single point of failure:** if the DB server dies, everything is down, and we might **lose data**.
- **Performance:** all reads and writes hit one machine. Most apps are **read-heavy** (people view far more than they post, often 10:1 to 100:1).

## 💡 The fix: replication (primary + replicas)
Keep **copies** of the database on several servers.
- **Primary (master):** accepts **all writes** (INSERT/UPDATE/DELETE).
- **Replicas (slaves/followers):** receive a copy of every change from the primary and serve **reads only**.
```
                       writes ──▶ [ PRIMARY DB ] ──replicates──┬──▶ [ Replica 1 ]
[web servers] ──┤                                              ├──▶ [ Replica 2 ]
                       reads ──────────────────────────────────┴──▶ (spread across replicas)
```

## ⚙️ How it works
1. The app sends writes to the primary.
2. The primary records each change in a log and streams it to the replicas.
3. The app sends reads (most of the traffic) to the replicas, spread across them.

What we gained:
- **Better read performance:** add replicas to scale reads.
- **Reliability:** data exists on several machines (ideally in different availability zones or data centers), so a disk failure or disaster doesn't lose it.
- **High availability:**
  - *A replica dies* → reads go to the other replicas (or temporarily to the primary). Replace it.
  - *The primary dies* → **promote a replica to be the new primary** (failover), then add a new replica.

## 🔀 Options
| Option | Notes |
|---|---|
| **Asynchronous replication** | The primary doesn't wait for replicas. Fast writes, but a replica can be slightly behind (**replication lag**). If the primary dies, the last few writes can be lost. The common default. |
| **Synchronous replication** | The primary waits for at least one replica to confirm. No data loss on failover, but slower writes. |
| **Primary-primary (multi-master)** | Two nodes both accept writes. Write availability, but **conflicts** need resolving. Complex. |
| Managed | Amazon RDS Multi-AZ (a synchronous standby for failover) + read replicas (async, for scaling reads) |

## ⚖️ Tradeoffs and pitfalls
- **Replication lag → stale reads.** A user updates their profile, refreshes, and sees the old value (they read from a lagging replica). Fix: **read-your-writes**, i.e. read from the primary for a short time after that user writes.
- Failover isn't instant and needs care: promoting an out-of-date replica can lose data, and two primaries at once ("split brain") is dangerous. Use managed failover or consensus (Raft).
- Replication **doesn't scale writes.** Every write still goes to one primary. That's [Step 12 (sharding)](12_database_sharding.md).

## 🗣️ Say it in an interview
> "Postgres with one primary for writes and two read replicas in other availability zones. Reads are 90% of the traffic, so the replicas take most of the load. Replication is async, so for read-your-writes I route a user's reads to the primary for a few seconds after they write. If the primary fails, a replica is promoted automatically."

## 🔗 Go deeper
- [Databases module: replication](../05_databases/) · [Fundamentals: availability patterns](../01_fundamentals/)
- Primer: [Master-slave replication](https://github.com/donnemartin/system-design-primer#master-slave-replication) · [Master-master replication](https://github.com/donnemartin/system-design-primer#master-master-replication)

## ✅ Self-check
- [ ] Draw primary + replicas and show where reads and writes go
- [ ] What happens when a replica dies? When the primary dies?
- [ ] What is replication lag, and how do you hide it from the user?
- [ ] Why doesn't replication help with write-heavy load?

**Next →** [Step 6: Cache](06_cache.md)
