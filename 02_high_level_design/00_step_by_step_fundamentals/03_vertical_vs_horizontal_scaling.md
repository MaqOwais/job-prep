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

**Next →** [Step 4: Load balancer](04_load_balancer.md)
