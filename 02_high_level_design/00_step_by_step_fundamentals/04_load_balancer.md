# Step 4 of 13: Load Balancer

[🏠 Overview](README.md) · **← Prev** [Step 3](03_vertical_vs_horizontal_scaling.md) · **Next →** [Step 5: Database replication](05_database_replication.md)

## 📍 Where we are
We decided to run **several web servers** (horizontal scaling). But:

## 🚨 The problem
- DNS gives users **one IP**. How do requests reach server 2 and server 3?
- If server 1 crashes, users connected to it get errors.
- Some servers might be overloaded while others sit idle.

## 💡 The fix: a load balancer (LB)
A load balancer sits in front of the servers. **Users only ever talk to the LB's public IP.** The LB forwards each request to a healthy server over a **private network**.
```
                         ┌──▶ [ web server 1 ] (private IP) ──┐
User ──▶ DNS ──▶ [ LOAD  ├──▶ [ web server 2 ] (private IP) ──┼──▶ [ Database ]
              (public IP) BALANCER ]                          │
                         └──▶ [ web server 3 ] (private IP) ──┘
```

## ⚙️ How it works
1. DNS points `myapp.com` to the **LB's public IP**.
2. The LB picks a server using an **algorithm** and forwards the request.
3. It runs **health checks** (e.g., `GET /health` every 10 s). An unhealthy server is removed from rotation automatically and added back when it recovers.
4. Servers have only **private IPs**, so they can't be reached directly from the internet (better security).

What we gained:
- **Failover:** server 1 dies → traffic goes to 2 and 3. Users don't notice.
- **Scalability:** traffic doubles → add servers 4 and 5 behind the LB (or let **autoscaling** do it).

## 🔀 Options
**Routing algorithms**
| Algorithm | When |
|---|---|
| Round robin | Servers are identical and requests are similar |
| Weighted round robin | Some servers are bigger |
| Least connections | Requests vary in duration (e.g., uploads) |
| IP hash / sticky sessions | The same user must reach the same server (avoid this; see Step 8) |
| Consistent hashing | Cache or shard affinity |

**Layer 4 vs layer 7**
| L4 (transport) | L7 (application) |
|---|---|
| Sees only IP + port | Sees the URL, headers, cookies |
| Very fast, simple | Smart routing: `/api/*` → API servers, `/images/*` → media servers |
| AWS NLB | AWS ALB, NGINX, Envoy |

## ⚖️ Tradeoffs and pitfalls
- **The LB can itself be a single point of failure.** Run a pair (active-passive or active-active), or use a managed LB, which is redundant internally.
- It adds a small extra network hop.
- **Sticky sessions** fight against free scaling (see [Step 8](08_stateless_web_tier.md)).

## 🗣️ Say it in an interview
> "An L7 load balancer in front of the web tier, with health checks across multiple availability zones. Servers sit in private subnets. That gives us failover and lets us autoscale."

## 🔗 Go deeper
- [Load balancing & reverse proxy module](../03_load_balancing_reverse_proxy/) (also covers consistent hashing)
- Primer: [Load balancer](https://github.com/donnemartin/system-design-primer#load-balancer) · [Layer 4](https://github.com/donnemartin/system-design-primer#layer-4-load-balancing) · [Layer 7](https://github.com/donnemartin/system-design-primer#layer-7-load-balancing)

## ✅ Self-check
- [ ] What problems does an LB solve? (3)
- [ ] How does an LB know a server is dead?
- [ ] L4 vs L7, with one use case each
- [ ] How do you stop the LB itself from being a single point of failure?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What problems does a load balancer solve?</b></summary>

1. **Distributes traffic** across many servers. 2. **Failover**: health checks remove dead servers automatically. 3. **Scalability**: add or remove servers without clients noticing. Bonus: SSL termination, a single public entry point (servers stay on private IPs), and connection draining during deploys.

</details>

<details>
<summary><b>Q2. Layer 4 vs layer 7 load balancing: what's the difference?</b></summary>

**L4** routes by IP and port (TCP/UDP) without looking at content: very fast, and supports static IPs (AWS NLB). **L7** understands HTTP: it can route by path, host, headers, or cookies, and can do auth, redirects, and rewrites (AWS ALB, NGINX). Use L7 for web apps and microservices, and L4 for raw TCP, extreme throughput, or non-HTTP protocols.

</details>

<details>
<summary><b>Q3. How do you stop the load balancer from becoming a single point of failure?</b></summary>

Run LBs redundantly: an **active-passive pair** with a floating IP and heartbeats, or **active-active** with DNS spreading traffic across them. Managed cloud LBs are already distributed across availability zones. For global setups, add DNS-level failover across regions.

</details>

<details>
<summary><b>Q4. Round robin vs least connections: when would you use each?</b></summary>

**Round robin** works when servers are identical and requests are short and similar. **Least connections** is better when request durations vary a lot (uploads, long polling, WebSockets), because it sends new work to the server with the fewest active requests.

</details>

<details>
<summary><b>Q5. What are sticky sessions, and why should you usually avoid them?</b></summary>

The LB pins a user to one server (by cookie or IP hash) because that server holds their session in memory. Problems: **uneven load**, sessions are **lost when that server dies** or is scaled in, and deployments get harder. Better: make servers stateless and keep sessions in Redis or a database.

</details>

**Next →** [Step 5: Database replication](05_database_replication.md)
