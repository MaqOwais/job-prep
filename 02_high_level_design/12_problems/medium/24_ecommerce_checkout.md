# 🟡 24. E-Commerce Platform: Cart & Checkout (Amazon-style)

📖 Related: [Microservices: saga, outbox](../../04_application_layer_microservices/) · [Payment system](../hard/19_payment_system.md) · [Ticketmaster (inventory holds)](23_ticketmaster.md)
⏱️ Try it yourself first: 40 minutes. **Very common at Amazon.**

## 1. Requirements
**Functional:** browse and search products; add to cart; checkout (address, payment); place an order; inventory decremented; order status tracking; notifications.
**Non-functional:** **the cart must always be available** (it drives revenue), no overselling of limited stock, peak traffic (Prime Day ~10× normal), orders never lost.

## 2. High-level design (microservices)
```
Client → CDN → LB → API gateway
  Catalog service   → product DB (document store) + Elasticsearch (search) + CDN images; heavy caching
  Cart service      → DynamoDB/Redis (key: user_id) — AP, always writable (Dynamo's original use case!)
  Pricing/Promo svc → rules engine, cached
  Checkout/Order orchestrator (saga):
        1. validate cart + price      2. reserve inventory (Inventory svc, strongly consistent, conditional decrement)
        3. authorize payment (Payment svc, idempotency key)   4. create order (Orders DB, SQL) → status PLACED
        on failure: compensate (release inventory, void payment authorization)
  Outbox → Kafka "order_placed" → Fulfillment/warehouse, Notifications (email/SMS), Analytics, Recommendations
```

## 3. Deep dives
- **Cart:** a highly available key-value store (the reason Amazon built Dynamo). Merge carts on login (guest + user). Conflicts on concurrent edits → union merge, as in the Dynamo paper.
- **Inventory without overselling:**
  - `UPDATE inventory SET qty = qty - n WHERE sku=? AND qty >= n` (atomic conditional decrement).
  - Hot SKUs during flash deals: split stock into **multiple sub-counters (buckets)** to spread the writes, or pre-allocate reservations in Redis.
  - Reserve at checkout and charge at shipment (authorize now, capture later).
- **Checkout = saga:** each step is a local transaction with a compensating action. Use the **outbox pattern** so events aren't lost; make every step **idempotent** (retries are safe).
- **Order IDs:** generated client-side or up front, plus idempotency keys, so a double-click doesn't create two orders.
- **Prime Day scale:** pre-scale, cache the catalog aggressively, put a queue in front of non-critical work, degrade gracefully (turn off recommendations before checkout fails).
- **Consistency split:** AP for cart, catalog, and reviews; CP for inventory, payments, and orders.

## ✅ Takeaways
AP cart (Dynamo-style) vs CP inventory/orders, **checkout saga with compensations + outbox**, conditional decrements for stock, idempotency everywhere.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why is the cart designed for availability rather than consistency?</b></summary>

Being unable to add to the cart **directly loses revenue**, while a rare inconsistency (e.g., a deleted item reappearing) is minor and fixable at checkout. Amazon built Dynamo for exactly this. Concurrent cart versions are merged (union).

</details>

<details>
<summary><b>Q2. How do you avoid overselling a limited-stock item?</b></summary>

An **atomic conditional decrement**: UPDATE inventory SET qty = qty - n WHERE sku=? AND qty >= n. For extremely hot SKUs (flash deals), split the stock into several sub-counters or pre-allocate tokens in Redis, and reserve at checkout with an expiry.

</details>

<details>
<summary><b>Q3. Walk through the checkout saga.</b></summary>

Validate the cart and price → **reserve inventory** → **authorize payment** (idempotency key) → **create the order** (PLACED) → emit OrderPlaced via the **outbox** → fulfillment, notifications, analytics. On failure, compensate: release the inventory and void the authorization.

</details>

<details>
<summary><b>Q4. How do you prevent duplicate orders from double-clicks or retries?</b></summary>

Generate an **order/idempotency key** on the client when checkout starts. The server stores key → result with a unique constraint, so repeated submissions return the same order instead of creating a new one.

</details>

<details>
<summary><b>Q5. How do you prepare for Prime Day traffic (10× normal)?</b></summary>

**Pre-scale** capacity and run load tests, cache the catalog and pricing aggressively, put queues in front of non-critical work, rate-limit, use feature flags to **degrade gracefully** (turn off recommendations before checkout), and have runbooks and on-call ready.

</details>
