# 6. Safety, Guardrails & Security

📖 [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) · [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)

## Threats
| Threat | What happens | Defenses |
|---|---|---|
| **Direct prompt injection / jailbreak** | User tries to override the system prompt ("ignore previous instructions…") | Input classifiers, strong system prompts, output checks, refusal training |
| **Indirect prompt injection** | Malicious instructions hidden in a **retrieved document, web page, email, or tool output** | Treat all retrieved content as **untrusted data**; least-privilege tools; human approval for sensitive actions; don't let content trigger tools on its own |
| **Data leakage** | Model reveals another user's or tenant's data, or the system prompt | **ACL filtering at retrieval**, tenant isolation, never put secrets in prompts |
| **PII exposure** | PII in prompts, logs, or outputs | PII detection and redaction (input + output + logs), data retention policies |
| **Hallucination** | Confident but false answers | RAG grounding, citations, groundedness checks, "I don't know" behavior, low temperature |
| **Excessive agency** | An agent takes harmful actions | Scoped tool permissions, confirmations, step and budget limits, audit logs |
| **Insecure output handling** | LLM output executed as code or SQL, or rendered as HTML | Validate and escape outputs, sandbox code execution, parameterized SQL |
| **Model denial of wallet** | Huge prompts or loops run up cost | Rate limits, token caps, per-user budgets |
| **Training data poisoning** | Bad data in fine-tuning or RAG sources | Source vetting, content review, eval gates |

## Guardrail architecture
```
User input → [input guardrails: auth, rate limit, PII redaction, injection/toxicity classifier, topic filter]
          → LLM (+ retrieval/tools with least privilege)
          → [output guardrails: toxicity, PII, groundedness check, schema validation, policy filter]
          → user                           (+ log everything, redacted)
```
Use **cheap fast classifiers first** and escalate to LLM-based checks only when needed (cost and latency).

## Enterprise requirements to mention
- Data isn't used for model training (Bedrock and enterprise API terms guarantee this; confirm current terms).
- **Private connectivity** (VPC endpoints / PrivateLink), encryption with customer-managed keys.
- Region pinning for data residency, audit trails, SOC 2 / HIPAA eligibility.
- Responsible AI: bias evaluation, transparency (it's AI), human escalation paths.

## ✅ Self-check
- [ ] Explain indirect prompt injection with an example (an email agent)
- [ ] Draw the guardrail pipeline
- [ ] How do you prevent cross-tenant leakage in RAG?
