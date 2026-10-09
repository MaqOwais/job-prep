# 🔴 11. AI Agent Platform (run customers' agents in production, like Bedrock AgentCore)

📖 Concepts: [Agents & tool use](../../concepts/03_agents_tool_use.md) · [Safety](../../concepts/06_safety_security.md) · [AWS GenAI stack](../../concepts/08_aws_genai_stack.md)
⏱️ Try it yourself first: 45 minutes. **Very relevant to AWS (AgentCore) and agent startups.**

## 1. Requirements
**Functional:** developers deploy agents written in any framework (LangGraph, CrewAI, Strands, custom code); the platform provides a runtime, **session isolation**, short- and long-term memory, a tool gateway (APIs and MCP servers), identity/auth for acting on behalf of users, code execution and browser sandboxes, and observability.
**Non-functional:** strong isolation between tenants and sessions (agents run untrusted code), long-running sessions (minutes to hours), scale to zero, low startup latency, auditability.

## 2. High-level design
```
Developer: package agent (container/code) → Registry → deploy → Agent endpoint
End user / app → API (authN: OAuth/OIDC) → Session router (session_id → sandbox)
   AGENT RUNTIME: one isolated microVM/container per SESSION (e.g. Firecracker), pre-warmed pool
        agent code runs here; calls the LLM via the model gateway; calls tools via the Tool Gateway
   TOOL GATEWAY: catalog of tools (REST APIs → MCP), auth injection (no secrets inside agent code),
        per-tool permissions & rate limits, input/output validation, audit log
   IDENTITY: user-delegated OAuth tokens (token vault) → agent acts with the USER's permissions only
   MEMORY SERVICE: short-term (session events) + long-term (extracted facts/preferences, vector + KV), per user/tenant namespaces
   SANDBOXES: code interpreter, headless browser (also isolated, egress-controlled)
   OBSERVABILITY: OpenTelemetry traces of every step (LLM calls, tool calls, tokens, latency, cost) → dashboards, eval
   POLICY: step/budget limits, human-approval hooks for sensitive tools, guardrails
```

## 3. Deep dives
- **Isolation:** containers share a kernel, so for untrusted multi-tenant code use **microVMs** (Firecracker) per session; restrict network egress; wipe state when the session ends.
- **Cold starts:** a pre-warmed sandbox pool and snapshot/restore of initialized VMs.
- **Long-running sessions:** durable session state, heartbeats, idle timeouts, and resuming from checkpoints.
- **Identity and auth (a key differentiator):** the agent never holds raw credentials. The gateway injects scoped tokens per tool call, the user consents once (OAuth), and every action is audited as "agent X on behalf of user Y".
- **Memory design:** event log → async extraction of durable facts (LLM summarization) → retrieval by relevance at session start. Namespaces per user; users can delete their memory.
- **MCP:** expose existing APIs as MCP tools through the gateway, so any framework can use them.
- **Billing and limits:** per-second compute for sandboxes + tokens + tool calls; per-tenant quotas.
- **Evaluation:** trace-based evals, task success rate, regression suites before deploying new agent versions; canary rollouts.

## ✅ Takeaways
**Per-session microVM isolation**, a tool gateway with **delegated identity**, a memory service, sandboxes, full tracing, and policy limits. This is how agents become production systems.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why run each agent session in its own microVM?</b></summary>

Agents execute **untrusted, model-generated code** and tool actions. Containers share the host kernel, so an escape could reach other tenants. **MicroVMs** (e.g., Firecracker) give hardware-level isolation per session with fast startup, plus restricted network egress and state wiped at session end.

</details>

<details>
<summary><b>Q2. How should an agent call third-party APIs on behalf of a user?</b></summary>

Through a **tool gateway** with **delegated identity**: the user grants OAuth consent once, tokens are kept in a vault, and the gateway injects a **scoped token** per call. The agent code never holds raw credentials, and every call is audited as "agent X on behalf of user Y".

</details>

<details>
<summary><b>Q3. How do you handle sessions that run for hours?</b></summary>

**Durable session state** and checkpoints, heartbeats, idle timeouts, resume after failure, and asynchronous patterns (the user gets notified when the task completes). Bill compute per second, and enforce maximum durations and budgets.

</details>

<details>
<summary><b>Q4. How do you design long-term memory for agents?</b></summary>

Store raw session events, then **asynchronously extract durable facts and preferences** (LLM summarization) into a per-user namespace (vector + KV). Retrieve the relevant memories at session start. Users and admins can view, correct, and delete them.

</details>

<details>
<summary><b>Q5. How do you safely release a new version of an agent?</b></summary>

Run **regression evals** on recorded traces and test suites, deploy as a **canary** to a small share of traffic, compare task success, cost, and safety metrics with the current version, roll out gradually, and keep instant rollback. Version prompts, tools, and models together.

</details>
