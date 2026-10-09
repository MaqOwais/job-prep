# Step 3 of 13: Vertical vs Horizontal Scaling

[🏠 Overview](README.md) · **← Prev** [Step 2](02_separate_database.md) · **Next →** [Step 4: Load balancer](04_load_balancer.md)

## 📍 Where we are
```
User ──▶ [ Web server ] ──▶ [ Database ]
```

## 🚨 The problem
The web server's CPU sits at 95%. Pages are slow. We need more capacity. There are two fundamentally different ways to get it.

## 💡 Option A: vertical scaling ("scale up")
**Make the machine bigger:** more CPU, more RAM, faster disks.
```
[ small server ]  ──upgrade──▶  [ HUGE server ]
```
✅ Very simple: no code changes, no new components.
❌ **There's a hard ceiling** (you can't add infinite CPU to one machine).
❌ Still a **single point of failure**. If it dies, everything's down.
❌ Large machines get disproportionately **expensive**.
❌ Upgrades often require **downtime**.

## 💡 Option B: horizontal scaling ("scale out")
**Add more machines** and spread the work across them.
```
                ┌─▶ [ server 1 ]
User ──▶ ? ─────┼─▶ [ server 2 ]
                └─▶ [ server 3 ]
```
✅ **Practically no ceiling.** Keep adding servers.
✅ **Redundancy:** if one dies, the others keep serving.
✅ Cheap commodity machines; **autoscaling** (add servers at peak, remove them at night).
❌ Needs new things: something to **distribute traffic** (Step 4), and servers that **don't keep local state** (Step 8).
❌ More operational complexity.

## ⚖️ Comparison
| | Vertical | Horizontal |
|---|---|---|
| How | Bigger machine | More machines |
| Limit | Hardware ceiling | Practically none |
| Failure | SPOF | Fault tolerant |
| Complexity | Low | Higher |
| Cost curve | Gets steep | Roughly linear |
| Best for | Early stage; databases (for a long time) | Web/app tiers at scale |

> **Real-world pattern:** scale **vertically first** (it's easy) until it gets expensive or the risk of a single point of failure matters. Scale the **stateless web tier horizontally** early. **Databases** are harder to scale horizontally, which is why Steps 5, 6, and 12 exist.

## 🗣️ Say it in an interview
> "Vertical scaling buys time but has a ceiling and a single point of failure. For the web tier I'll scale horizontally behind a load balancer, which means the servers must be stateless."

## 🔗 Go deeper
- [Fundamentals: performance vs scalability](../01_fundamentals/) · Primer: [Horizontal scaling](https://github.com/donnemartin/system-design-primer#horizontal-scaling) · [Performance vs scalability](https://github.com/donnemartin/system-design-primer#performance-vs-scalability)

## ✅ Self-check
- [ ] Give 3 drawbacks of vertical scaling
- [ ] What 2 things does horizontal scaling require?
- [ ] Why are databases harder to scale horizontally than web servers?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Compare vertical and horizontal scaling.</b></summary>

**Vertical** = a bigger machine: simple, no code changes, but there's a hardware ceiling, it's still a SPOF, and cost grows steeply. **Horizontal** = more machines: practically no ceiling, redundancy, autoscaling, but it needs a load balancer and stateless services, and it's more complex to operate.

</details>

<details>
<summary><b>Q2. Why is it easier to scale web servers horizontally than databases?</b></summary>

Web servers can be **stateless**: any server can handle any request, so you just add copies. Databases **own state**. Copies must stay in sync (replication), and splitting data across machines (sharding) breaks joins and transactions and needs rebalancing.

</details>

<details>
<summary><b>Q3. A startup's single server is at 90% CPU. What do you do first, and why?</b></summary>

Measure first (profile: is it CPU in the app, slow queries, or memory?). Quick wins: fix hot queries and add indexes, then **scale vertically** for immediate relief. In parallel, make the app stateless and put it behind a load balancer so it can scale horizontally. Vertical buys time; horizontal is the long-term answer.

</details>

<details>
<summary><b>Q4. What is autoscaling, and what metrics would you scale on?</b></summary>

Automatically adding or removing instances based on load. Typical signals: **CPU utilization**, request count per target, **latency**, and **queue depth** for workers. Use target tracking (e.g., keep CPU at 60%), scheduled scaling for known peaks, and cooldowns to avoid flapping.

</details>

<details>
<summary><b>Q5. Is vertical scaling ever the right long-term answer?</b></summary>

Yes, often for **databases**. Modern machines are huge (hundreds of cores, TBs of RAM), and a vertically scaled primary with read replicas can serve very large products for years. That's simpler than sharding. It's also fine for workloads that are hard to distribute, like some in-memory analytics.

</details>

**Next →** [Step 4: Load balancer](04_load_balancer.md)
