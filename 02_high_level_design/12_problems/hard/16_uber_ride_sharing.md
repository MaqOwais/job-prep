# 🔴 16. Uber / Lyft: Ride Sharing

📖 Related: [Uber engineering: H3 hexagonal index](https://www.uber.com/blog/h3/) · primer [Real-world architectures](https://github.com/donnemartin/system-design-primer#real-world-architectures)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** riders request a ride; nearby drivers are matched; drivers send their location every few seconds; riders see the driver's location live; trip lifecycle (requested → accepted → in progress → completed); pricing, including surge pricing; payment.
**Non-functional:** matching in seconds, a **very high write rate** of location updates, high availability, no double-booking a driver (consistency on assignment).

## 2. Estimates
1M active drivers sending a location every 4 s → **250K writes/s**. Rider requests: ~1K/s at peak.

## 3. High-level design
```
Driver app ─(WebSocket/HTTP, every 4s)→ Location service → in-memory geo index (Redis GEO / H3 cells)
                                                └→ Kafka (location stream → analytics, ETA, surge)
Rider app → Ride service → Matching service
                              1. query geo index: drivers in nearby cells, available
                              2. rank by ETA (routing service) 
                              3. offer to driver (with timeout) → accept → atomically lock the driver
           ← push trip updates via WebSocket gateway
Trip service (state machine, SQL)  ·  Pricing/Surge service  ·  Payment service  ·  Maps/ETA service
```

## 4. Deep dives
- **Geospatial indexing (the core problem):**
  - **Geohash:** a base32 string where a shared prefix means nearby. Query the cell + its 8 neighbors.
  - **Quadtree:** adapts to density (splits busy areas into smaller cells).
  - **H3 (Uber):** hexagonal cells with uniform neighbor distances.
  - Store the **latest location in memory** (Redis GEO, sharded by city/region). Don't write every ping to the DB; send the raw stream to Kafka for history.
- **Matching consistency:** a driver must not get 2 trips. Use an atomic compare-and-set on driver status (Redis Lua, or a DB row lock / conditional write) with an offer timeout.
- **Sharding by geography:** city or region as the partition unit keeps matching local.
- **Surge pricing:** stream-compute supply/demand per cell (Flink) → price multiplier.
- **Failure handling:** if a location server dies, drivers reconnect and state rebuilds within seconds from the next pings (the data is ephemeral).
- **Trip state and payments:** strongly consistent store + idempotent payments ([payment system](19_payment_system.md)).

## ✅ Takeaways
In-memory **geo index (geohash/quadtree/H3)**, a location stream that never writes every ping to the DB, **atomic driver locking**, and sharding by city.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do you find the nearest available drivers quickly?</b></summary>

Keep drivers' **latest locations in memory** in a geospatial index (Redis GEO, geohash cells, or H3 hexagons), sharded by city or region. A query reads the rider's cell + its neighbors, filters by availability, then ranks by **ETA** from the routing service.

</details>

<details>
<summary><b>Q2. How do you handle 250K location updates per second?</b></summary>

Drivers send updates over persistent connections to stateless **location services** that overwrite the in-memory index (only the latest position matters) and publish to **Kafka** for history and analytics. No synchronous DB write per ping.

</details>

<details>
<summary><b>Q3. How do you make sure a driver isn't assigned two trips at once?</b></summary>

**Atomic state transition** on the driver: compare-and-set from AVAILABLE to OFFERED/ASSIGNED (Redis Lua script or a conditional DB update) with an **offer timeout**. Only one matcher can win, and an expired offer returns the driver to AVAILABLE.

</details>

<details>
<summary><b>Q4. How is surge pricing computed?</b></summary>

A stream processor (Flink) computes **supply vs demand per geo cell** over short windows (open requests vs available drivers) and produces a price multiplier per cell, smoothed to avoid flapping. The pricing service reads it when quoting.

</details>

<details>
<summary><b>Q5. Why shard by city or region?</b></summary>

Matching is **local**: riders only need nearby drivers. Partitioning by geography keeps queries on one shard, isolates failures, and lets you place services near users. Trips crossing boundaries are handled at the edges.

</details>
