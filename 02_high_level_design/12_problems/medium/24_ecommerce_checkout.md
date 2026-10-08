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
