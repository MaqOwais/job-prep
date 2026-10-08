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
