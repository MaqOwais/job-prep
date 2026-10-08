# 8. The AWS GenAI Stack (for AWS / cloud interviews)

Use these names when designing on AWS. They map one-to-one onto the generic concepts in modules 1–7.
Related: [AWS SA prep plan](../../06_company_specific/aws_startup_sa/AWS_Associate_Startup_SA_Prep_Plan.md) · [Bedrock docs](https://docs.aws.amazon.com/bedrock/)

> ⚠️ AWS launches and renames GenAI services frequently. Check [What's New with AWS](https://aws.amazon.com/new/) before your interview.

## Generic concept → AWS service
| Concept | AWS service |
|---|---|
| Foundation model API (many providers) | **Amazon Bedrock** (Anthropic Claude, Amazon Nova, Meta Llama, Mistral, Cohere, …) |
| Managed RAG (chunking, embedding, vector store, retrieval) | **Bedrock Knowledge Bases** |
| Vector store | OpenSearch Serverless, Aurora PostgreSQL + pgvector, **S3 Vectors**, Neptune Analytics (GraphRAG), or partners (Pinecone etc.) |
| Agents / tool use | **Bedrock Agents**; **Bedrock AgentCore** (runtime, memory, gateway for tools/MCP, identity, code interpreter, browser, observability) for running agents built with any framework |
| Guardrails | **Bedrock Guardrails** (content filters, denied topics, PII redaction, contextual grounding checks) |
| Prompt management / flows | Bedrock Prompt Management, Bedrock Flows |
| Evaluation | Bedrock model and RAG evaluation; SageMaker Clarify |
| Fine-tuning / customization | Bedrock model customization (fine-tuning, continued pretraining, **distillation**); SageMaker training (incl. HyperPod for large-scale training) |
| Self-hosted model serving | **SageMaker AI endpoints** (real-time, serverless, async, batch), EKS/ECS + vLLM on GPU instances |
| Cheaper AI chips | **AWS Inferentia** (inference), **AWS Trainium** (training) |
| Throughput guarantees | Bedrock Provisioned Throughput; cross-region inference profiles; batch inference (cheaper) |
| Cost and latency | Bedrock **prompt caching**, intelligent prompt routing, batch inference |
| Orchestration / durable workflows | Step Functions, EventBridge, SQS, Lambda |
| Feature store / ML pipelines | SageMaker Feature Store, SageMaker Pipelines, Model Registry, Model Monitor |
| Document parsing | Amazon Textract, Bedrock Data Automation |
| Speech | Amazon Transcribe (speech-to-text), Amazon Polly (text-to-speech), Nova Sonic (speech-to-speech) |
| Private connectivity | VPC endpoints / PrivateLink to Bedrock; KMS encryption |
| Observability | CloudWatch (incl. GenAI observability), X-Ray, CloudTrail for audit |
| Developer AI assistants | Amazon Q Developer, Kiro |

## Reference architecture: serverless RAG on AWS
```
S3 (docs) ──event──▶ Bedrock Knowledge Base (parse → chunk → Titan/Cohere embeddings → OpenSearch Serverless / S3 Vectors)

User ─▶ CloudFront ─▶ API Gateway (WebSocket/REST, Cognito auth, throttling)
     ─▶ Lambda / ECS Fargate orchestrator
          ├─ Bedrock Guardrails (input)
          ├─ KB Retrieve (metadata filter: tenant_id, groups)  → re-rank
          ├─ Bedrock InvokeModelWithResponseStream (Claude) + prompt caching
          ├─ Bedrock Guardrails (output, contextual grounding)
          └─ DynamoDB (chat history)   · CloudWatch/X-Ray traces · S3 feedback logs → eval
```

## Talking points for AWS interviews
- "Bedrock doesn't use customer prompts or outputs to train models, and the data stays in your AWS region and account boundary." (Confirm the current wording on the Bedrock security page.)
- "Start serverless with Knowledge Bases to ship fast. Move to custom chunking, re-ranking, or self-hosted models only where the evals show you need them."
- "For a startup, prompt caching + model routing + batch inference typically give the biggest cost wins."
- Connect to **Well-Architected**: there's a **Generative AI Lens**.
