# Step 8 of 13: Stateless Web Tier

[🏠 Overview](README.md) · **← Prev** [Step 7](07_cdn.md) · **Next →** [Step 9: Multiple data centers](09_multiple_data_centers.md)

## 📍 Where we are
```
User ──▶ CDN (static)
User ──▶ LB ──▶ [web 1][web 2][web 3] ──▶ cache ──▶ DB primary + replicas
```

## 🚨 The problem: stateful servers
Say each web server keeps the **user's session** (login state, cart) **in its own memory**.
```
Alice logs in → LB sends her to web 1 → session stored in web 1's memory
Next request → LB sends her to web 2 → web 2 has never heard of her → "please log in again" ❌
```
Workarounds hurt:
- **Sticky sessions** (the LB always sends Alice to web 1) → uneven load, and if web 1 dies or is removed during autoscaling, **Alice's session is gone**.
- We can't freely **add or remove** servers. Autoscaling breaks.

## 💡 The fix: move state out of the web servers
Store session and user state in a **shared data store**. Every web server reads it from there.
```
                         ┌──▶ [web 1] ──┐
User ──▶ LB (any server) ├──▶ [web 2] ──┼──▶ [ SHARED SESSION STORE: Redis / DynamoDB ]
                         └──▶ [web 3] ──┘
```
Now **any server can handle any request**. Web servers become interchangeable "cattle, not pets".

## ⚙️ How it works
- On login, create a session → store `session:{id} → {user_id, cart, …}` in Redis with a TTL → send the session ID to the client in a secure cookie.
- Each request: read the cookie → look up the session in Redis → serve.
- Alternative: **stateless tokens (JWT)**. The signed token carries the user's claims, so the server needs no lookup. The tradeoff: tokens are hard to revoke, so keep their expiry short.

## 🎁 What this unlocks
- **Autoscaling:** add servers at peak and remove them at night, and no user notices.
- **Failure tolerance:** a server crash loses nothing.
- **Simple deployments:** rolling, blue/green, and canary releases just swap servers.
- It's a prerequisite for [multiple data centers](09_multiple_data_centers.md).

## ⚖️ Pitfalls
- The session store is now critical, so make it highly available (replicated Redis or DynamoDB).
- "Stateless" applies to the **web tier**. State still exists, but it lives in purpose-built stores (DB, cache, object storage, session store).
- Also move other local state out: **uploaded files → S3** (not the local disk), and scheduled jobs → a central scheduler.

## 🗣️ Say it in an interview
> "Web servers are stateless. Sessions live in Redis and files in S3. So any server can serve any request, we can autoscale freely, and a crashed server loses nothing."

## 🔗 Go deeper
- [Load balancing module (horizontal scaling)](../03_load_balancing_reverse_proxy/) · [Security: sessions vs JWT](../09_security/)
- Primer: [Horizontal scaling](https://github.com/donnemartin/system-design-primer#horizontal-scaling)

## ✅ Self-check
- [ ] Why do stateful servers break horizontal scaling?
- [ ] Why are sticky sessions a weak fix?
- [ ] Session store vs JWT: tradeoffs

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What makes a web server 'stateful', and why is that a problem for scaling?</b></summary>

It keeps client data (sessions, carts, uploaded files) in **local memory or disk**, so a user must keep returning to the same server. That breaks load balancing, autoscaling (removing a server loses sessions), and failover.

</details>

<details>
<summary><b>Q2. How do you make the web tier stateless?</b></summary>

Move all state to shared stores: **sessions → Redis/DynamoDB** (or self-contained JWTs), **files → object storage (S3)**, persistent data → the database, scheduled work → a central scheduler or queue. Then any server can serve any request.

</details>

<details>
<summary><b>Q3. Server-side sessions vs JWT: compare them.</b></summary>

**Server-side session**: an opaque ID cookie plus a lookup in a session store. Easy to revoke, small cookie, but every request needs a store lookup. **JWT**: a signed token carrying the claims, verified without any lookup, which makes it stateless and fast. But it's **hard to revoke** before expiry and larger. Use short-lived JWTs with refresh tokens.

</details>

<details>
<summary><b>Q4. What does a stateless web tier enable operationally?</b></summary>

**Autoscaling** in and out, **zero-downtime deployments** (rolling, blue/green, canary), instant replacement of unhealthy instances, multi-AZ and multi-region serving, and simpler load balancing with no sticky sessions.

</details>

<details>
<summary><b>Q5. If the web tier is stateless, where does the risk move to?</b></summary>

To the **shared state stores** (session store, database, cache, object storage). They must be highly available (replicated, multi-AZ) and scalable, because every request now depends on them.

</details>

**Next →** [Step 9: Multiple data centers](09_multiple_data_centers.md)
