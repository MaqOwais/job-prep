# 11. The System Design Interview Framework

📖 Primer: [How to approach a system design interview question](https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question) · [Study guide](https://github.com/donnemartin/system-design-primer#study-guide)

Use these steps for **every** design question, out loud, in this order.

---

## Step 1: Requirements and scope (5 min)
**Functional:** what can users do? Pick the 3–4 core features and confirm them.
**Non-functional:** scale (DAU, QPS), latency targets, availability vs consistency, durability, read:write ratio, global vs regional.

Questions to ask:
- Who are the users and how many? Expected growth?
- What are the most important features for this interview?
- Read-heavy or write-heavy?
- Does it need to be real-time? Is consistency or availability more important?
- Any constraints (mobile, global, compliance)?

✍️ Write the requirements on the board. **Explicitly mark what's out of scope.**

## Step 2: Back-of-envelope estimation (3–5 min)
QPS (average and peak), storage per year, bandwidth, cache size (the 80/20 rule: cache the hot 20%). See [estimation](../10_estimation/).

## Step 3: API design (3–5 min)
```
POST /v1/tweets           {text, media_ids}           → 201 {tweet_id}
GET  /v1/timeline?cursor=…&limit=20                    → 200 {tweets[], next_cursor}
```
Include auth, pagination, and idempotency keys where needed.

## Step 4: Data model (3–5 min)
Entities, key fields, primary/partition keys, **which DB and why** (tie it to the access patterns).

## Step 5: High-level design (10 min)
Draw the boxes:
```
Client → DNS → CDN
       → Load Balancer → API Gateway → [Service A] [Service B]
                                          │           │
                                     Cache (Redis)  Queue (Kafka) → Workers
                                          │           │
                                        DB (SQL/NoSQL)   Object storage (S3)
```
Walk through **one write path and one read path** end to end.

## Step 6: Deep dives (15–20 min)
Let the interviewer steer, or pick the hardest parts yourself:
- Scaling the DB (sharding key, replicas)
- Caching strategy and invalidation
- Hot keys / celebrity problem
- Consistency model, race conditions, idempotency
- Real-time delivery (WebSockets)
- Ranking or search algorithms

## Step 7: Bottlenecks, failures, wrap-up (5 min)
- What fails first at 10× load? SPOFs?
- Failure modes: node down, region down, queue backup, retries + DLQ
- Monitoring: metrics, logs, tracing, alerting
- Security: auth, rate limiting, encryption
- **Summarize the design in 30 seconds**, and mention what you'd improve with more time.

---

## 🏆 What separates strong answers
| Weak | Strong |
|---|---|
| Starts drawing immediately | Clarifies requirements and scale first |
| "Use NoSQL because it scales" | "Access pattern X → partition key Y → Cassandra" |
| One design, no alternatives | "Option A vs B; I pick A because…" |
| Ignores failures | Discusses retries, idempotency, failover |
| Silent | Narrates their thinking and checks in with the interviewer |
| Over-engineers from day one | Starts simple, then scales step by step |

## 🔁 Practice method
1. Set a 45-minute timer. Use paper or Excalidraw.
2. Do all 7 steps out loud (record yourself).
3. Compare with the problem notes in [12_problems](../12_problems/) and the primer solution.
4. List 3 things you missed, and redo the problem 3 days later.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What are the steps of a system design interview, in order?</b></summary>

1) **Requirements** (functional + non-functional, scope), 2) **estimation**, 3) **API design**, 4) **data model**, 5) **high-level design** (walk a read and a write path), 6) **deep dives** on 2–3 hard parts, 7) **bottlenecks, failures, tradeoffs**, and a summary.

</details>

<details>
<summary><b>Q2. Which non-functional requirements should you always ask about?</b></summary>

Scale (users, QPS, data size, growth), latency targets, **availability vs consistency**, durability, read:write ratio, geographic distribution, security and compliance, and cost constraints.

</details>

<details>
<summary><b>Q3. How do you handle an interviewer who keeps changing requirements?</b></summary>

Treat it as the test: **acknowledge** the change, restate the new constraint, explain **what in the design changes and why** (e.g., "now strong consistency → move bookings to a transactional store"), and keep the rest. It shows adaptability and understanding of the tradeoffs.

</details>

<details>
<summary><b>Q4. What do strong candidates do differently in deep dives?</b></summary>

They **choose** the riskiest component, discuss **alternatives with tradeoffs**, tie choices to the requirements and numbers, cover failure modes (retries, idempotency, failover), and check in with the interviewer instead of monologuing.

</details>

<details>
<summary><b>Q5. How should you end a design interview?</b></summary>

A **30-second summary** of the architecture and key decisions, the known **bottlenecks and how you'd evolve** the design at 10× scale, what you'd monitor, and what you'd do with more time. Then ask your questions.

</details>
