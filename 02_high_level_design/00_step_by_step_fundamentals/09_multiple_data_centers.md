# Step 9 of 13: Multiple Data Centers

[🏠 Overview](README.md) · **← Prev** [Step 8](08_stateless_web_tier.md) · **Next →** [Step 10: Message queue](10_message_queue.md)

## 📍 Where we are
A solid, stateless, cached, replicated system, but **all in one data center**.

## 🚨 The problem
- A data center (or a whole cloud region) can go down: power, network, fire, a bad config push. **The entire app is offline.**
- Users on other continents still have high latency for **dynamic** requests (the CDN only helps with static files).

## 💡 The fix: run in multiple data centers
```
                         GeoDNS / global LB
                        (route to nearest healthy DC)
                    ┌──────────────┴──────────────┐
             ┌──────▼──────┐                ┌──────▼──────┐
             │   DC US-East │                │   DC EU-West │
             │ LB → web tier│                │ LB → web tier│
             │ cache        │                │ cache        │
             │ DB (primary) │◀══replication══▶│ DB           │
             └─────────────┘                └─────────────┘
```

## ⚙️ How it works
- **GeoDNS / geo-routing:** DNS answers with the IP of the data center **closest to the user** (or by latency or a weighting).
- **Failover:** if DC US-East fails its health checks, DNS sends **all** traffic to EU-West.
- **Data replication across data centers:** each DC needs the data. Replicate asynchronously between them (cross-continent round trips are 100+ ms, so synchronous writes would be painfully slow).

> **Cloud vocabulary:** in AWS, an **availability zone (AZ)** is one or more data centers. A **region** contains 3+ AZs. "Multi-AZ" (the same region, ms apart) is the standard for HA. "Multi-region" is for disaster recovery and global latency.

## 🔀 Patterns
| Pattern | How | Tradeoff |
|---|---|---|
| **Active-passive** | One region serves traffic; the other is a standby (pilot light / warm standby) | Simpler; failover takes minutes; standby resources are wasted |
| **Active-active** | All regions serve traffic | Best latency and availability; **write conflicts** and data consistency are hard |
| **Geo-partitioned** | EU users' data lives in the EU region | Data residency compliance (GDPR); cross-region features are harder |

## ⚖️ Technical challenges
- **Traffic redirection:** GeoDNS and health checks, with DNS TTLs short enough for fast failover.
- **Data synchronization:** async replication means a failover can lose the last few seconds of writes. Active-active needs conflict resolution (last-write-wins, CRDTs, or per-record home regions).
- **Testing and deployment:** keep the regions identical with **infrastructure as code** and automated deploys to all of them. **Regularly test failover**, or it won't work when you need it.
- **Cost:** you pay for the infrastructure (at least) twice.

## 🗣️ Say it in an interview
> "Within a region I'd deploy across 3 availability zones for HA. For disaster recovery and global latency I'd add a second region, active-passive to start, with async DB replication and DNS failover. Active-active comes later if latency demands it, with data partitioned by home region to avoid write conflicts."

## 🔗 Go deeper
- [Fundamentals: availability patterns, CAP](../01_fundamentals/) · [AWS: DR strategies](../../06_company_specific/aws_startup_sa/AWS_Associate_Startup_SA_Prep_Plan.md)
- Primer: [Availability patterns](https://github.com/donnemartin/system-design-primer#availability-patterns) · [DNS](https://github.com/donnemartin/system-design-primer#domain-name-system)

## ✅ Self-check
- [ ] How do users get routed to the nearest data center?
- [ ] Active-passive vs active-active
- [ ] Why is cross-region replication usually asynchronous, and what's the risk?
- [ ] AZ vs region

**Next →** [Step 10: Message queue](10_message_queue.md)
