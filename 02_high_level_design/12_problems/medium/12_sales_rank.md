# 🟡 12. Amazon Sales Rank by Category

📖 Primer solution: [Design Amazon's sales rank by category feature](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** compute the top-selling products per category over the past week (rank updated hourly); users view the top N per category.
**Non-functional:** read-heavy for views, 1B transactions/month of input, results can be up to an hour stale.

## 2. Estimates
1B sales/month → ~400 transactions/s written. 100B reads/month → ~40K read QPS → **cache the results**.

## 3. High-level design
```
Orders service → sales logs (S3 / Kafka)
                     ▼ hourly
          Batch job (MapReduce / Spark):
             map:    (category, product_id) → quantity
             reduce: sum per (category, product)
             sort:   by category, then quantity desc → top N
                     ▼
          sales_rank table (SQL: category_id, product_id, total_sold, rank)
                     ▼
Client → CDN → Read API → Redis cache → sales_rank DB
```

## 4. Deep dives
- **Batch vs streaming:** the primer uses an hourly batch, which is simple and reliable. Modern alternative: **Flink/Kafka Streams** with sliding windows for near-real-time ranks.
- **Top-k per category:** a min-heap of size k per category (see [heaps](../../../01_coding/09_heap_priority_queue/)), or a distributed sort.
- **Approximate counting** at massive scale: **Count-Min Sketch** + heap (the heavy-hitters problem).
- **Sliding 7-day window:** keep daily aggregates and sum the last 7 days (cheap) instead of reprocessing every raw log.
- **Serving:** precomputed results are tiny, so cache them at the CDN and in Redis.

## ✅ Takeaways
Offline aggregation (MapReduce) → precomputed tables → heavy caching. Mention streaming and Count-Min Sketch as upgrades.
