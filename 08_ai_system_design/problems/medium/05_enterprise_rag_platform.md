# 🟡 05. Enterprise RAG Platform (ChatGPT-style assistant over company docs)

📖 Concepts: [RAG & retrieval](../../concepts/02_rag_retrieval.md) · [Safety](../../concepts/06_safety_security.md) · [Evaluation](../../concepts/05_evaluation_observability.md) · [AWS GenAI stack](../../concepts/08_aws_genai_stack.md)
📖 Related: [AWS: What is RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/) · [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) · [Anthropic: Contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
⏱️ Try it yourself first: 45 minutes. **This plays directly to your agentic AI research. Expect it at AI-focused companies and AWS.**

## 1. Requirements
**Functional:** users ask questions in natural language and get answers **grounded in company documents** with citations; streaming responses; chat history; document ingestion (PDF, HTML, Confluence); per-user access control on documents; optional tool use / agents.
**Non-functional:** time to first token < 1–2 s, accurate (few hallucinations), secure (no data leaks across tenants), cost-efficient (GPU and token costs), observable (quality evaluations).

## 2. Estimates
100K daily active users × 10 questions = 1M queries/day → ~12 QPS average, ~50 peak.
Each query ≈ 3K input tokens (context) + 500 output tokens → **token cost and GPU capacity dominate**, not QPS.

## 3. High-level design
```
INGESTION (async):
Docs (S3/Confluence) → event → Queue → Parser (PDF/HTML → text) → Chunker (≈500 tokens, overlap)
   → Embedding model (batch) → Vector DB (pgvector / OpenSearch / Pinecone) + metadata (doc_id, ACL, tenant)
   → also keyword index (BM25) for hybrid search

QUERY:
Client ⇄ (SSE/WebSocket stream) → API Gateway (auth, rate limit) → Orchestrator service
   1. input guardrails (PII, prompt injection, policy)
   2. query rewrite (use chat history to make it standalone)
   3. retrieve: hybrid search (vector + BM25) filtered by user ACL → top 50
   4. re-rank (cross-encoder) → top 5–8 chunks
   5. build prompt (system + context + question + citations format)
   6. LLM call (Bedrock / self-hosted vLLM on GPUs) → stream tokens
   7. output guardrails (grounding check, PII redaction) → client
   8. log trace (prompt, chunks, latency, tokens, feedback) → eval pipeline
Chat history: DynamoDB/Redis   ·   Semantic cache (embedding similarity) for repeated questions
```

## 4. Deep dives
- **Prompting vs RAG vs fine-tuning:** RAG for fresh or private facts; fine-tuning for style, format, or domain behavior; usually RAG first.
- **Retrieval quality is most of the battle:** chunking strategy, hybrid search, re-ranking, contextual chunk headers, metadata filters.
- **Security:** enforce ACLs **at retrieval time** (filter by tenant and user groups); never rely on the LLM to hide data. Defend against prompt injection, and give tools least privilege.
- **Serving and cost:** model routing (a small model for easy queries, a large one for hard queries), prompt caching, a semantic response cache, batching, quantization; GPU autoscaling on queue depth; provisioned throughput for a steady base load.
- **Latency:** stream tokens (SSE), run retrieval in parallel, keep the context lean.
- **Evaluation:** offline golden datasets (faithfulness, answer relevance, retrieval recall@k), LLM-as-judge, online thumbs up/down, A/B testing of prompts and models.
- **Agents (your research angle):** orchestrator/router → specialized agents/tools (search, SQL, APIs) with step limits, timeouts, human approval for risky actions, and tracing of every step.

## ✅ Takeaways
Async ingestion → hybrid retrieval with **ACL filtering** → re-rank → streamed generation with guardrails → evaluation loop. Talk about **cost and quality**, not just boxes.
