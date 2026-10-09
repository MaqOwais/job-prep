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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Batch or streaming for computing sales ranks?</b></summary>

**Batch** (hourly MapReduce/Spark) is simple, cheap, and reliable when hourly freshness is OK. **Streaming** (Flink/Kafka Streams with sliding windows) gives near-real-time ranks but is more complex. Start with batch; move to streaming if the business needs fresher ranks.

</details>

<details>
<summary><b>Q2. How do you compute a rolling 7-day window efficiently?</b></summary>

Keep **daily aggregates** per (category, product) and sum the last 7 days, instead of reprocessing raw logs each time. Each hour, only today's partial aggregate changes.

</details>

<details>
<summary><b>Q3. How do you find the top-k products per category?</b></summary>

Aggregate counts per (category, product), then keep a **min-heap of size k** per category (O(n log k)), or do a distributed sort by (category, count desc) and take the first k per group.

</details>

<details>
<summary><b>Q4. How do you serve 40K read QPS for the rankings?</b></summary>

The results are small and precomputed. Store them in a **DB table** and serve through a **Redis cache and CDN**, refreshed when the batch job finishes. Reads never touch the aggregation pipeline.

</details>

<details>
<summary><b>Q5. What if the number of distinct products is too large to count exactly?</b></summary>

Use streaming **heavy-hitters algorithms**: Count-Min Sketch for approximate counts + a heap for the top-k, or Space-Saving. They use bounded memory and accept a small error, which is fine for rankings.

</details>
