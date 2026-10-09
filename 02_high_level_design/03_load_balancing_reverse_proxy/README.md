# 3. Load Balancing & Reverse Proxy

📖 Primer: [Load balancer](https://github.com/donnemartin/system-design-primer#load-balancer) · [Active-passive](https://github.com/donnemartin/system-design-primer#active-passive) · [Layer 4 load balancing](https://github.com/donnemartin/system-design-primer#layer-4-load-balancing) · [Layer 7 load balancing](https://github.com/donnemartin/system-design-primer#layer-7-load-balancing) · [Horizontal scaling](https://github.com/donnemartin/system-design-primer#horizontal-scaling) · [Reverse proxy](https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server) · [LB vs reverse proxy](https://github.com/donnemartin/system-design-primer#load-balancer-vs-reverse-proxy)

---

## 3.1 Load balancer (LB)
Distributes incoming requests across healthy servers.
**Benefits:** no single unhealthy server takes traffic, horizontal scaling, SSL termination, session persistence.
LBs can themselves be a SPOF, so run them **active-passive or active-active**.

### Algorithms
| Algorithm | Notes |
|---|---|
| Round robin / weighted round robin | Simple; the weighted version accounts for bigger machines |
| Least connections | Good when requests take different amounts of time |
| Least response time | Considers latency |
| IP hash / consistent hashing | Sticky routing (same user → same server, or cache affinity) |
| Random with two choices | Pick 2 servers at random, send to the less loaded one. Surprisingly good. |

### Layer 4 vs Layer 7
| | L4 (transport) | L7 (application) |
|---|---|---|
| Looks at | IP + port | URL, headers, cookies, body |
| Can | Forward packets (NAT) | Route `/api` → service A, `/video` → service B; auth; rewrite |
| Speed | Faster, less CPU | Slower but smarter |
| AWS | NLB | ALB |

### Horizontal scaling needs
- **Stateless app servers.** Keep sessions in Redis/DB, not in memory.
- Health checks, plus connection draining during deploys.
- Downsides: more complexity, and the DB/cache downstream must also handle the extra load.

## 3.2 Consistent hashing (very common in interviews)
Problem: with `hash(key) % N`, changing N remaps almost every key, so the cache stampedes.
Solution: put servers and keys on a **hash ring**. Each key goes to the next server clockwise. Adding or removing a server moves only about **1/N of the keys**.
**Virtual nodes:** each physical server owns many points on the ring, which gives a more even distribution.
Used in Dynamo, Cassandra, memcached clients, and CDNs.

## 3.3 Reverse proxy
A server in front of your backends that forwards client requests and returns responses. Examples: **NGINX, HAProxy, Envoy**.
**Benefits:** hides the backends (security), SSL termination, compression, caching of static content, serving static files, rate limiting.

**LB vs reverse proxy:** an LB is useful with **multiple** servers. A reverse proxy is useful even with **one** server. NGINX/HAProxy can do both.

**API Gateway** = reverse proxy + auth + rate limiting + request routing + aggregation (Kong, AWS API Gateway).

## 🗣️ Say it in an interview
> "An L7 load balancer in front of stateless app servers, with sessions in Redis, so we can autoscale horizontally. For the cache tier I'd use consistent hashing with virtual nodes, so adding a cache node only remaps about 1/N of the keys."

## ✅ Self-check
- [ ] L4 vs L7: give one use case for each
- [ ] Explain consistent hashing and virtual nodes with a drawing
- [ ] LB vs reverse proxy vs API gateway

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Load balancer vs reverse proxy vs API gateway: what's the difference?</b></summary>

A **reverse proxy** sits in front of servers (even one) and handles TLS, caching, compression, and hides the backends. A **load balancer** is a reverse proxy whose main job is spreading traffic across many servers with health checks. An **API gateway** adds API concerns: authentication, rate limiting, request routing to microservices, transformation, and API keys.

</details>

<details>
<summary><b>Q2. Explain consistent hashing and why virtual nodes are used.</b></summary>

Servers and keys are hashed onto a ring, and each key belongs to the next server clockwise. Adding or removing a server only moves keys in **one segment (~1/N)**, unlike hash % N, which remaps almost everything. **Virtual nodes** (many ring points per server) spread load evenly and make it easy to weight bigger servers.

</details>

<details>
<summary><b>Q3. How does a load balancer handle a deploy without dropping requests?</b></summary>

**Connection draining**: mark the instance as deregistering, stop sending it new requests, let in-flight requests finish (up to a timeout), then stop it. Combined with health checks and rolling or blue/green deploys, users see no errors.

</details>

<details>
<summary><b>Q4. What is 'power of two choices' load balancing?</b></summary>

Pick **two servers at random** and send the request to the less loaded one. It's almost as good as a global least-loaded choice, but needs no central state, which makes it scale well across many load balancers. It's used in Envoy and NGINX variants.

</details>

<details>
<summary><b>Q5. When would you choose an NLB (L4) over an ALB (L7)?</b></summary>

For non-HTTP protocols (raw TCP/UDP, gaming, MQTT), when you need **static IPs** or extreme throughput with ultra-low latency, or when you want TLS passthrough end to end. Use ALB for HTTP routing, host/path rules, WebSockets, and auth integration.

</details>
