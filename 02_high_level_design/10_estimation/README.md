# 10. Back-of-the-Envelope Estimation

📖 Primer: [Appendix](https://github.com/donnemartin/system-design-primer#appendix) · [Powers of two table](https://github.com/donnemartin/system-design-primer#powers-of-two-table) · [Latency numbers every programmer should know](https://github.com/donnemartin/system-design-primer#latency-numbers-every-programmer-should-know)

---

## 10.1 Powers of two
| Power | Exact | Approx | Bytes |
|---|---|---|---|
| 2¹⁰ | 1,024 | 1 thousand | 1 KB |
| 2²⁰ | 1,048,576 | 1 million | 1 MB |
| 2³⁰ | | 1 billion | 1 GB |
| 2⁴⁰ | | 1 trillion | 1 TB |
| 2⁵⁰ | | 1 quadrillion | 1 PB |

## 10.2 Latency numbers (orders of magnitude)
| Operation | Time |
|---|---|
| L1 cache reference | 0.5 ns |
| Main memory reference | 100 ns |
| Compress 1 KB (fast codec) | ~2–10 µs |
| Send 1 KB over a 1 Gbps network | 10 µs |
| SSD random read | ~16–150 µs |
| Read 1 MB sequentially from memory | ~250 µs |
| Round trip within the same datacenter | 500 µs (0.5 ms) |
| Read 1 MB sequentially from SSD | ~1 ms |
| Disk seek (HDD) | 10 ms |
| Read 1 MB sequentially from HDD | ~20–30 ms |
| Packet round trip CA → Netherlands → CA | 150 ms |

**Takeaways:** memory is fast, disk is slow, and **avoid cross-continent round trips**. Compress before sending. Sequential reads are much faster than random ones.

## 10.3 Handy conversions
- **1 day ≈ 86,400 s ≈ 10⁵ s** (round it to 100K)
- 1 month ≈ 2.5 million seconds
- **1 million requests/day ≈ 12 QPS** (10⁶ / 86,400)
- 100M requests/day ≈ 1,200 QPS
- **Peak ≈ 2–3× the average**
- Read-heavy apps: about a 10:1 to 100:1 read:write ratio

## 10.4 Typical sizes
| Item | Size |
|---|---|
| char (ASCII) / UTF-8 average | 1 B / 1–4 B |
| int / long / UUID | 4 B / 8 B / 16 B |
| Tweet text | ~140–300 B |
| Metadata row | ~1 KB |
| Image (compressed) | ~200 KB–2 MB |
| 1 minute of HD video | ~50–100 MB |

## 10.5 Single-server capacity (very rough)
- Web/app server: ~1K–10K QPS (simple requests)
- PostgreSQL/MySQL: ~1K–10K writes/s, more reads with caching
- Redis: ~100K+ ops/s per node
- Kafka: ~100K–1M messages/s per cluster (scales with partitions)

## 10.6 The estimation recipe (worked example: Twitter)
1. **Users:** 300M monthly active, 150M daily active.
2. **Writes:** 150M users × 2 tweets/day = 300M tweets/day → **~3,500 tweets/s** (peak ~7K).
3. **Reads:** each user loads the timeline 10×/day → 1.5B/day → **~17K QPS** (peak ~35K+).
4. **Storage:** 300M tweets × 300 B ≈ **90 GB/day** of text → ~33 TB/year (media stored separately, much bigger).
5. **Bandwidth:** 17K reads/s × 20 tweets × 300 B ≈ **100 MB/s** egress for text.

> Round aggressively. State assumptions clearly. Interviewers care about the **method and the order of magnitude**, not exact arithmetic.

## ✅ Self-check
- [ ] Convert 50M requests/day → QPS (≈ 580)
- [ ] Estimate storage for 1B photos at 500 KB each (≈ 500 TB)
- [ ] Say 5 latency numbers from memory

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Convert 100 million requests per day into QPS, and estimate the peak.</b></summary>

100M ÷ ~100K seconds per day (86,400 rounded up) ≈ **1,000–1,200 QPS average**. Peak ≈ 2–3× → **~2,500–3,500 QPS**. Round aggressively and state your assumptions.

</details>

<details>
<summary><b>Q2. Estimate the storage for 500M users each uploading 2 photos per day at 300 KB.</b></summary>

Assume 10% are daily uploaders: 50M × 2 × 300 KB = **30 TB/day** → ~11 PB/year (before replicas and thumbnails; replication ×3 → ~33 PB). The point is showing the method: users × actions × size × time × replication.

</details>

<details>
<summary><b>Q3. Why does it matter that a memory read is ~100 ns but a cross-continent round trip is ~150 ms?</b></summary>

It's a gap of over a **million times**. Design decisions follow from it: cache in memory, keep chatty calls inside one data center, batch requests, use CDNs and regional deployments, and avoid synchronous cross-region calls on the hot path.

</details>

<details>
<summary><b>Q4. How do you estimate the number of servers needed?</b></summary>

Peak QPS ÷ the QPS one server can handle (measure, or assume ~1–5K for simple API calls), then add **headroom** (×1.5–2) and N+1 or multi-AZ redundancy. Example: 30K peak ÷ 2K per server = 15 → ~25–30 across 3 AZs.

</details>

<details>
<summary><b>Q5. What's the right level of precision in estimation?</b></summary>

**Orders of magnitude**: is it 10 GB or 10 TB? 100 QPS or 100K? Round to friendly numbers, say the assumptions out loud, and use the result to drive decisions (fits in memory? needs sharding? needs a CDN?). Exact arithmetic wastes interview time.

</details>
