# 2. RAG & Retrieval

**RAG (Retrieval-Augmented Generation):** retrieve relevant documents → put them in the prompt → the LLM answers **grounded** in them, with citations. It reduces hallucinations and keeps knowledge fresh without retraining.

## The pipeline
```
OFFLINE (ingestion):  load → parse → clean → CHUNK → (enrich) → EMBED → INDEX (vector + keyword) + metadata
ONLINE (query):       query → rewrite → RETRIEVE (hybrid, filtered) → RE-RANK → build prompt → GENERATE → cite
```

## Chunking
| Strategy | Notes |
|---|---|
| Fixed-size (e.g. 300–800 tokens, 10–20% overlap) | Simple baseline |
| Structure-aware (headings, paragraphs, code blocks, tables) | Usually better: chunks follow the document's meaning |
| Semantic chunking | Split where the embedding similarity drops |
| Parent-child / small-to-big | Retrieve small precise chunks, then send the larger parent section to the LLM |
| **Contextual chunk headers** | Prepend doc title or section, or an LLM-generated context sentence, to each chunk before embedding ([Anthropic: contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)) |

Too small → loses context. Too big → diluted embeddings and wasted tokens.

## Embeddings
- Model choice: domain fit, dimension (384–3072), multilingual support, cost. Benchmarks: the [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard).
- **Re-embed everything if you change the embedding model.** Version your indexes.
- Similarity: cosine or dot product.

## Vector indexes (ANN = approximate nearest neighbor)
| Index | How | Tradeoff |
|---|---|---|
| Flat (brute force) | Compare against everything | Exact; fine for < ~100K vectors |
| **HNSW** | Multi-layer proximity graph | Fast and accurate; memory-heavy; the most popular |
| IVF | Cluster vectors, then search only the nearest clusters | Less memory; tune `nprobe` |
| PQ (product quantization) | Compress vectors | Huge scale, some accuracy loss |

**Vector stores:** pgvector (Postgres), OpenSearch / Elasticsearch, Pinecone, Weaviate, Milvus, Qdrant, Amazon S3 Vectors, FAISS (a library).
> Interview tip: "If they already run Postgres and have < 10M vectors, **pgvector** keeps the stack simple."

## Retrieval quality techniques (ranked by impact)
1. **Hybrid search:** BM25 keyword search + vector search, merged with **Reciprocal Rank Fusion**. Catches exact terms (error codes, names) that embeddings miss.
2. **Re-ranking:** a cross-encoder re-scores the top 50–100 → keep the top 5–10. Large precision gain.
3. **Metadata filters:** tenant, ACL, date, document type. **Apply ACL filters at retrieval time.**
4. **Query rewriting:** make follow-up questions standalone using chat history. **HyDE** (embed a hypothetical answer). Multi-query expansion.
5. Better chunking and contextual headers.
6. **Agentic / iterative retrieval:** the LLM decides whether it needs more searches (more latency, better for complex questions).

## Advanced variants
- **GraphRAG:** build a knowledge graph of entities and relations; good for "connect the dots" questions.
- **Long-context instead of RAG:** with 1M-token windows, sometimes you can just put everything in. Tradeoffs: cost, latency, and "lost in the middle" effects. Prompt caching helps.
- **Structured data:** text-to-SQL instead of embeddings for tables and metrics.

## Failure modes to mention
Retrieved the wrong chunk (retrieval failure) vs had the right chunk but answered wrong (generation failure). **Measure them separately** (see [evaluation](05_evaluation_observability.md)). Also: stale index, duplicate documents, PDF parsing errors (tables!), multilingual mismatches.

## ✅ Self-check
- [ ] Draw the ingestion and query pipelines
- [ ] HNSW vs IVF in 2 sentences
- [ ] Why hybrid search + re-ranking?
- [ ] Where do you enforce document permissions, and why there?
