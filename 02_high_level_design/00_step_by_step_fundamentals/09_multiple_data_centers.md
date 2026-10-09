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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How are users routed to the right data center, and how does failover work?</b></summary>

**GeoDNS / latency-based DNS** (or a global anycast load balancer) returns the IP of the nearest healthy data center. Health checks detect a failed DC, and DNS stops returning it, so traffic shifts to the remaining DCs. Short DNS TTLs speed up failover.

</details>

<details>
<summary><b>Q2. Active-passive vs active-active across regions?</b></summary>

**Active-passive**: one region serves traffic and the other is a standby that takes over on failure. Simpler, minutes of downtime, idle capacity. **Active-active**: all regions serve traffic, giving lower latency and instant failover, but writes in multiple regions create **conflicts** and need careful data design (home regions, CRDTs, last-write-wins).

</details>

<details>
<summary><b>Q3. Why is cross-region database replication usually asynchronous?</b></summary>

Synchronous writes would wait for a cross-continent round trip (~100+ ms) on **every write**, and stall if the link degrades. Async keeps writes fast. The tradeoff is a small **RPO** (seconds of writes lost if a region fails) and eventual consistency between regions.

</details>

<details>
<summary><b>Q4. What's the difference between an availability zone and a region?</b></summary>

An **AZ** is one or more isolated data centers with independent power and networking. AZs in the same region are a few ms apart. A **region** is a geographic area containing multiple AZs. Multi-AZ protects against data center failures (the HA standard). Multi-region protects against regional disasters and serves global users.

</details>

<details>
<summary><b>Q5. What are the hardest operational challenges of running multiple data centers?</b></summary>

**Data synchronization and consistency**, keeping configs and deployments identical (infrastructure as code, automated multi-region deploys), **testing failover regularly** (otherwise it fails when needed), data residency rules, and roughly doubling infrastructure cost.

</details>

**Next →** [Step 10: Message queue](10_message_queue.md)
