# 🟢 02. Semantic Search (e.g., product or document search by meaning)

📖 Concepts: [RAG & retrieval](../../concepts/02_rag_retrieval.md) · Related classic problem: [Search engine](../../../02_high_level_design/12_problems/medium/14_search_engine.md)
⏱️ Try it yourself first: 30 minutes.

## 1. Requirements
**Functional:** users search with natural language ("waterproof shoes for hiking in winter") and get relevant results even without exact keyword matches; filters (price, category); results in < 300 ms.
**Non-functional:** 10M items, 1K QPS, new items searchable within minutes.

## 2. Estimates
10M items × 768 dims × 4 bytes ≈ **30 GB** of vectors (less with quantization). HNSW adds memory overhead. That fits a small sharded cluster.

## 3. High-level design
```
INDEXING: Catalog DB → CDC/stream → embedding workers (batch, GPU or API) → vector index (HNSW) + BM25 index + filterable metadata
QUERY:    Client → API → query embedding (cached for popular queries)
              → hybrid retrieval: ANN top-200 (with metadata filters) ∪ BM25 top-200 → Reciprocal Rank Fusion
              → re-rank top-100 (cross-encoder or learning-to-rank with business signals) → top-20 → response
```

## 4. Deep dives
- **Why hybrid:** embeddings miss exact tokens (SKUs, brand names, sizes). BM25 misses synonyms. Together they cover both.
- **Filtering:** pre-filter vs post-filter on ANN results. Post-filtering can return too few results; prefer vector DBs with filtered HNSW.
- **Latency:** cache query embeddings, keep the index in memory, shard by item hash, use replicas for QPS.
- **Freshness:** stream new items into the index incrementally; rebuild periodically.
- **Model updates:** a new embedding model means re-embedding everything into a new index version, then switching over (blue/green).
- **Evaluation:** offline nDCG@10 and recall@k on labeled query-item pairs; online click-through rate, add-to-cart rate, zero-result rate.

## ✅ Takeaways
Embeddings + ANN (HNSW) + BM25 hybrid + re-ranking, with filtered search, index versioning, and nDCG/CTR evaluation.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why does pure vector search miss queries like 'error E-4012'?</b></summary>

Embedding models compress meaning and often don't preserve **exact rare tokens** (codes, SKUs, names). Keyword search (BM25) matches them exactly, which is why hybrid search is the standard.

</details>

<details>
<summary><b>Q2. Pre-filtering vs post-filtering with metadata filters?</b></summary>

**Post-filtering** (ANN first, then filter) can return too few results if the filter is selective. **Pre-filtering** (restrict candidates first) is accurate but can be slow with naive ANN. Prefer vector DBs that support **filtered HNSW** search natively.

</details>

<details>
<summary><b>Q3. How do you roll out a new embedding model?</b></summary>

Embeddings from different models aren't compatible, so **re-embed the whole corpus into a new index version**, evaluate it offline (nDCG/recall), A/B test it, then switch traffic over (blue/green) and delete the old index.

</details>

<details>
<summary><b>Q4. How much memory do 10M vectors of 768 dimensions need?</b></summary>

10M × 768 × 4 bytes (float32) ≈ **30 GB**, plus the HNSW graph overhead (often 1.5–2×). Quantization (float16/int8/PQ) reduces it 2–8×. Shard it across nodes if needed.

</details>

<details>
<summary><b>Q5. How do you measure search quality?</b></summary>

Offline: **nDCG@10, recall@k, MRR** on labeled query-result pairs. Online: click-through rate, add-to-cart or conversion rate, **zero-result rate**, query reformulation rate, and time to click.

</details>
