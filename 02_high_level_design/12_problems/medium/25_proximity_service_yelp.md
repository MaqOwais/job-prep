# 🟡 25. Proximity Service (Yelp / Google Maps "restaurants near me")

📖 Related: [Uber (moving objects)](../hard/16_uber_ride_sharing.md) · [Geohash explained](https://en.wikipedia.org/wiki/Geohash) · [Uber H3](https://www.uber.com/blog/h3/)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** search businesses near a location within a radius (500 m–20 km), with filters (category, open now, rating); view business details; owners add and update businesses.
**Non-functional:** 100M daily active users, ~5K search QPS, < 200 ms latency. Business data changes rarely (updates can appear the next day), so it's very read-heavy.

## 2. Key idea: a spatial index
Querying `WHERE lat BETWEEN … AND lng BETWEEN …` with two separate indexes is inefficient. Options:

| Index | How | Notes |
|---|---|---|
| **Geohash** | Encode (lat, lng) as a base32 string; a shared prefix means nearby | Simple and works in any DB or Redis. Query the cell + its 8 neighbors (handles edge cases). Precision by length: 6 chars ≈ 1.2 × 0.6 km. |
| **Quadtree** | Recursively split regions until each has ≤ N businesses | Adapts to density (Manhattan vs desert). Built in memory. |
| **S2 / H3** | Hierarchical sphere cells (Google) / hexagons (Uber) | Production-grade, good for coverings |
| PostGIS / Elasticsearch geo | Built-in geo queries | Easiest when the scale is moderate |

## 3. High-level design
```
Client → LB → Location-based service (LBS, stateless, read-only)
              1. compute geohash of user location at a precision matching the radius
              2. fetch business_ids for that cell + 8 neighbors (from geo index: Redis / in-memory / DB table geohash→ids)
              3. load details (cache) → filter exact distance (haversine) + filters → rank (distance, rating) → page
Business service (CRUD for owners) → Business DB (SQL primary + read replicas)
   nightly/periodic job rebuilds geo index → replicated to all LBS nodes (fits in memory: 200M businesses × ~ 50 B ≈ 10 GB)
```

## 4. Deep dives
- **Radius → precision:** pick the geohash length whose cell size matches the radius. If too few results come back, widen to a shorter prefix.
- **Boundary problem:** two nearby points can have different prefixes, which is why you always include the 8 neighboring cells.
- **Read scaling:** the geo index is small and read-only, so replicate it everywhere (no sharding needed). Cache popular areas.
- **Updates:** rarely changing data → periodic rebuild is fine. Real-time updates would need an incremental index.
- **Contrast with Uber:** Yelp has **static** points (a periodically rebuilt index). Uber has **moving** points (an in-memory index with updates every few seconds).

## ✅ Takeaways
**Geohash/quadtree** spatial indexing, query the cell + neighbors, an exact distance filter, a read-only replicated index.
