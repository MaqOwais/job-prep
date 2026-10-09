# 🟡 14. Search Engine / Full-Text Search Service

📖 Related: [Web crawler](07_web_crawler.md) · primer [Real-world architectures: Google, Elasticsearch](https://github.com/donnemartin/system-design-primer#real-world-architectures)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** search documents by keywords; ranked results; pagination; snippets.
**Non-functional:** < 200 ms p99, billions of documents, new documents searchable within minutes.

## 2. Core data structure: the inverted index
```
"cloud"  → [(doc3, tf=4, positions=[1,9,..]), (doc17, tf=1, …), …]
"aws"    → [(doc3, …), (doc42, …)]
```
Build it with tokenization → lowercasing → stopword removal → stemming → posting lists sorted by doc_id (compressed, e.g. delta + varint encoding).

## 3. High-level design
```
Indexing:  crawler/content → Kafka → Indexer (tokenize, build segments) → Index shards (+ replicas)
Querying:  Client → LB → Query service (parse, spell-correct)
               → scatter to all index shards → each returns its local top-k
               → gather + merge (heap) → re-rank → fetch snippets → response
           + result cache (Redis) for popular queries
```

## 4. Deep dives
- **Sharding the index:**
  - **Document-partitioned** (each shard holds a subset of documents with a full index): every query hits every shard (scatter-gather), but writes are easy. **The common choice** (Elasticsearch).
  - Term-partitioned (each shard holds certain terms): fewer shards per query, but multi-term queries cross shards and hot terms create hotspots.
- **Ranking:** TF-IDF / **BM25** for relevance + PageRank/quality signals + freshness → ML learning-to-rank on the top candidates (two-phase ranking).
- **Near-real-time indexing:** small in-memory segments flushed and merged periodically (Lucene's design).
- **Replication:** replicas per shard scale read QPS and provide HA.
- **Tail latency:** with many shards the slowest shard dominates, so use hedged requests and timeouts with partial results.

## ✅ Takeaways
Inverted index, document-partitioned shards, scatter-gather with top-k merging, BM25 + re-ranking, caching hot queries.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What is an inverted index?</b></summary>

A map from each **term** to a **posting list** of the documents containing it (with term frequency and positions). Built by tokenizing, normalizing, and stemming documents. A query intersects or unions the posting lists to find candidate documents.

</details>

<details>
<summary><b>Q2. Document-partitioned vs term-partitioned index sharding?</b></summary>

**Document-partitioned:** each shard indexes a subset of documents fully, so queries go to **all shards** (scatter-gather) but indexing is easy and load is balanced. This is the common choice. **Term-partitioned:** each shard owns certain terms, so queries touch fewer shards, but multi-term queries cross shards and popular terms create hotspots.

</details>

<details>
<summary><b>Q3. What is BM25?</b></summary>

A relevance scoring function improving on TF-IDF: it rewards term frequency with **saturation** (diminishing returns), weights rare terms higher (IDF), and normalizes by **document length**. It's the default lexical ranking in Lucene and Elasticsearch.

</details>

<details>
<summary><b>Q4. How do you make new documents searchable within minutes?</b></summary>

**Near-real-time indexing**: write new documents into small in-memory segments that are refreshed every second or so, then flush and merge segments in the background (Lucene's design). Feed it from Kafka.

</details>

<details>
<summary><b>Q5. With 100 shards, one slow shard makes every query slow. What do you do?</b></summary>

Tail-latency techniques: **replicas** per shard with **hedged requests** (send to a second replica if the first is slow), per-shard timeouts that return partial results, load-aware routing, and keeping shards evenly sized.

</details>
