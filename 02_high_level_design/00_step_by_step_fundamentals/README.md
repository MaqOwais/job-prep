# 🧱 HLD Fundamentals, Step by Step: From One Server to Millions of Users

**Read this before anything else in high-level design.**
Instead of memorizing components, we **grow one system** (a simple web app) from 1 user to millions. At every step something breaks, and we add **exactly one** component to fix it. By the end you'll know *why* each building block exists, which is what interviewers actually test.

> Inspired by the "scale from zero to millions" chapter in Alex Xu's *System Design Interview* (Vol. 1) and the [System Design Primer](https://github.com/donnemartin/system-design-primer). Read those too. The explanations here are my own notes.

## 🗺️ The journey
| Step | We hit this problem… | …so we add | Read |
|---|---|---|---|
| 1 | We need *something* running | **A single server + DNS** | [01_single_server.md](01_single_server.md) |
| 2 | App and data fight over one machine | **A separate database** (and pick SQL vs NoSQL) | [02_separate_database.md](02_separate_database.md) |
| 3 | The one server is maxed out | **Vertical vs horizontal scaling** | [03_vertical_vs_horizontal_scaling.md](03_vertical_vs_horizontal_scaling.md) |
| 4 | Many servers: who gets which request? And what if one dies? | **Load balancer** | [04_load_balancer.md](04_load_balancer.md) |
| 5 | The single database is a bottleneck and a single point of failure | **Database replication** | [05_database_replication.md](05_database_replication.md) |
| 6 | Same reads hit the DB again and again | **Cache** | [06_cache.md](06_cache.md) |
| 7 | Users far away wait for images and JS | **CDN** | [07_cdn.md](07_cdn.md) |
| 8 | Servers remember user sessions, so we can't add or remove them freely | **Stateless web tier** | [08_stateless_web_tier.md](08_stateless_web_tier.md) |
| 9 | One data center = one region's outage takes us down | **Multiple data centers** | [09_multiple_data_centers.md](09_multiple_data_centers.md) |
| 10 | Slow tasks block requests; components are tightly coupled | **Message queue** | [10_message_queue.md](10_message_queue.md) |
| 11 | We can't see, debug, or deploy safely at this size | **Logging, metrics, automation** | [11_logging_metrics_automation.md](11_logging_metrics_automation.md) |
| 12 | The database is still too big and write-heavy | **Sharding** | [12_database_sharding.md](12_database_sharding.md) |
| 13 | Recap: the full architecture | **Everything together** | [13_putting_it_together.md](13_putting_it_together.md) |

## How each step is written
Every file has the same sections:
1. **📍 Where we are:** the architecture so far (diagram)
2. **🚨 The problem:** what breaks, concretely
3. **💡 The fix:** the new component, in plain words
4. **⚙️ How it works:** the mechanics
5. **🔀 Options:** types and variants of the component
6. **⚖️ Tradeoffs and pitfalls:** what this costs and what can go wrong
7. **🗣️ Say it in an interview:** a ready-made sentence
8. **🔗 Go deeper:** the detailed concept module + primer sections
9. **✅ Self-check**

## How to study it
- **Day 1:** read steps 1–7. **Day 2:** steps 8–13.
- After each step, **close the file and draw the new diagram from memory**, then say out loud *why* the new component was needed.
- The final test: draw [the full architecture](13_putting_it_together.md) from memory in 10 minutes, narrating each addition. This is also the answer to the classic "scale to millions of users" question ([AWS version](../12_problems/easy/04_scale_to_millions_aws.md)).

**Next →** [Step 1: A single server](01_single_server.md)
