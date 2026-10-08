# 🤖 AI / LLM System Design

AI-focused companies (OpenAI, Anthropic, Scale, Perplexity, AI startups) and cloud providers (AWS, especially Bedrock and Startups SA roles) now ask **AI system design** questions alongside or instead of classic ones. This folder builds on [02_high_level_design](../02_high_level_design/). You still need load balancers, queues, and caches, but the interesting parts are different: **retrieval quality, GPU cost, latency to first token, evaluation, and safety**.

> 💡 This is where your resume stands out: multi-agent orchestrator/router systems, LangChain, LLM APIs, VAEs/KDE research, and AWS pipelines. Use those projects as examples in your answers.

## How AI design interviews differ
| Classic system design | AI system design |
|---|---|
| QPS and storage dominate the estimates | **Tokens, GPU memory, and $/request** dominate |
| Correctness is binary | Quality is **probabilistic**, so you need an **evaluation strategy** |
| Latency = p99 response time | **Time to first token (TTFT)** + tokens/second + total latency |
| Security = auth + encryption | Also **prompt injection, data leakage, jailbreaks, hallucinations** |
| Scale by adding servers | GPUs are scarce and expensive: batching, caching, model routing, quantization |
| Deterministic tests | Offline eval sets + online A/B tests + human feedback loops |

## 🧭 The framework (adapted from the [classic one](../02_high_level_design/11_interview_framework/))
1. **Clarify the use case and success metric.** Who uses it? What does "good" mean (accuracy, helpfulness, deflection rate, revenue)? What's the latency budget and cost budget per request?
2. **Is an LLM even the right tool?** Rules, classic ML, or search might be cheaper. Saying this earns points.
3. **Estimate:** requests/day × tokens in/out → tokens/s → GPUs needed or API cost per month.
4. **Model strategy:** API model (Bedrock, OpenAI, Anthropic) vs open-weights self-hosted. Prompting → RAG → fine-tuning → (rarely) pretraining.
5. **High-level design:** ingestion/data pipeline, online serving path, storage, orchestration.
6. **Deep dives:** retrieval quality, serving efficiency, agents/tools, safety.
7. **Evaluation and monitoring:** offline eval set, online metrics, feedback loop, drift.
8. **Cost, failure modes, and iteration plan:** fallbacks when the model or provider is down, cost controls, how v2 improves.

## 📚 Concept modules (read these first)
| # | Module | What you'll be able to explain |
|---|---|---|
| 1 | [LLM fundamentals](concepts/01_llm_fundamentals.md) | Tokens, transformers, context windows, sampling, embeddings, cost and latency math |
| 2 | [RAG & retrieval](concepts/02_rag_retrieval.md) | Chunking, embeddings, vector indexes (HNSW/IVF), hybrid search, re-ranking |
| 3 | [Agents & tool use](concepts/03_agents_tool_use.md) | Agent loop, ReAct, multi-agent orchestrator/router patterns, MCP, memory |
| 4 | [LLM serving & inference](concepts/04_llm_serving_inference.md) | KV cache, continuous batching, vLLM, quantization, speculative decoding, GPU autoscaling |
| 5 | [Evaluation & observability](concepts/05_evaluation_observability.md) | Offline and online evals, LLM-as-judge, RAG metrics, tracing |
| 6 | [Safety, guardrails & security](concepts/06_safety_security.md) | Prompt injection, PII, jailbreaks, hallucination mitigation, tenant isolation |
| 7 | [Classic ML system design](concepts/07_classic_ml_system_design.md) | Feature stores, training pipelines, online vs batch inference, drift, A/B testing |
| 8 | [AWS GenAI stack](concepts/08_aws_genai_stack.md) | Bedrock, Knowledge Bases, Agents/AgentCore, Guardrails, SageMaker, Inferentia/Trainium |

## 🧪 Problems: Easy → Medium → Hard
| Level | # | Problem | Core concepts |
|---|---|---|---|
| 🟢 | 01 | [Customer support chatbot](problems/easy/01_customer_support_chatbot.md) | Prompting, conversation memory, escalation to humans |
| 🟢 | 02 | [Semantic search](problems/easy/02_semantic_search.md) | Embeddings, vector DB, hybrid search |
| 🟢 | 03 | [Content moderation service](problems/easy/03_content_moderation.md) | Classifier cascade, cheap → expensive models, human review |
| 🟡 | 04 | [LLM gateway](problems/medium/04_llm_gateway.md) | Multi-provider routing, rate limits, caching, fallbacks, cost tracking |
| 🟡 | 05 | [Enterprise RAG platform](problems/medium/05_enterprise_rag_platform.md) | Ingestion, ACL-aware retrieval, re-ranking, guardrails, evals |
| 🟡 | 06 | [AI coding assistant (Copilot)](problems/medium/06_ai_coding_assistant.md) | Low-latency completion, context building, FIM, acceptance metrics |
| 🟡 | 07 | [Recommendation system](problems/medium/07_recommendation_system.md) | Candidate generation + ranking, feature store, two-tower models |
| 🟡 | 08 | [Multi-agent research assistant](problems/medium/08_multi_agent_research_assistant.md) | Orchestrator/router, specialized agents, tools, **your research** |
| 🔴 | 09 | [LLM inference platform](problems/hard/09_llm_inference_platform.md) | GPU fleet, continuous batching, multi-model serving, autoscaling |
| 🔴 | 10 | [Fine-tuning platform](problems/hard/10_fine_tuning_platform.md) | Multi-tenant training jobs, LoRA, data pipelines, eval gates |
| 🔴 | 11 | [AI agent platform (AgentCore-style)](problems/hard/11_agent_platform.md) | Sandboxed execution, tool gateway, identity, memory, observability |
| 🔴 | 12 | [Real-time voice agent](problems/hard/12_realtime_voice_agent.md) | Speech-to-text → LLM → text-to-speech streaming, < 1 s latency, interruptions |

## 🔗 Resources
- [Chip Huyen, *AI Engineering*](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) and *Designing Machine Learning Systems*: the two best books for this round
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [vLLM docs](https://docs.vllm.ai/) · [PagedAttention paper](https://arxiv.org/abs/2309.06180)
- [Eugene Yan: patterns for LLM systems](https://eugeneyan.com/writing/llm-patterns/)
- [Hello Interview: ML system design](https://www.hellointerview.com/learn/ml-system-design/in-a-hurry/introduction)
- [AWS Generative AI on AWS](https://aws.amazon.com/generative-ai/) · [Amazon Bedrock docs](https://docs.aws.amazon.com/bedrock/)

> ⚠️ This field moves fast. Model names, prices, and service features change monthly. Check the current state before an interview and say "as of my last check…" when quoting numbers.
