# 🟡 08. Multi-Agent Research Assistant ("Deep Research"-style)

📖 Concepts: [Agents & tool use](../../concepts/03_agents_tool_use.md) · [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)
⏱️ Try it yourself first: 40 minutes.

> 💡 **Your research problem.** You built orchestrator, router, analyst, creation, manager, and skill-based data-fetching agents. Practice explaining this design **using your own system as the example**: "In my VR-therapy project, the router agent…"

## 1. Requirements
**Functional:** the user asks a complex question ("Compare the top 5 vector databases for a startup: cost, scale, features") → the system plans, searches the web and internal sources, reads documents, analyzes data, and writes a cited report. Progress updates while it works.
**Non-functional:** minutes per task is acceptable, but it must be **reliable** (no infinite loops), cost-bounded, accurate (citations), and resumable after failures.

## 2. High-level design
```
User → API → Task service (creates task_id, durable state in DB) → returns stream of progress events (SSE)
                  ↓
        ORCHESTRATOR / LEAD AGENT (strong model)
          1. clarify + plan: break into sub-questions, decide which specialists
          2. dispatch in PARALLEL → worker agents (cheaper/faster models), each with its own context:
               • Search agent  (web search tool, internal KB retrieval)
               • Reader agent  (fetch + extract from pages/PDFs)
               • Analyst agent (code-interpreter sandbox for data/charts)
          3. collect compressed findings (not raw pages) → decide: enough? or another round
          4. Writer agent → report draft → Citation/verifier agent checks claims against sources
        Tools behind a TOOL GATEWAY (MCP servers): search, fetch, KB, sandbox — with auth, rate limits, timeouts
        Durable workflow engine (Step Functions / Temporal): checkpoints after each step → resume on crash
        Tracing of every agent step (tokens, cost, tool calls)
```

## 3. Deep dives
- **Why multi-agent here?** Research splits naturally into parallel, independent subtasks, and separate context windows avoid overflowing a single agent. The cost is **many more tokens**, so justify it with the task's value.
- **Context management:** workers return **condensed findings with source URLs**, not full documents. The orchestrator keeps a compact plan plus notes in memory.
- **Control:** max agents, max steps, per-task token and $ budget, timeouts per tool, a stop condition ("enough evidence").
- **Quality:** source quality ranking, a citation verifier (is each claim supported?), conflicting-source handling.
- **Safety:** fetched web pages may contain **prompt injection** → treat them as data; workers have no dangerous tools.
- **Failure handling:** retries per tool call, durable checkpoints, partial results if the budget runs out.
- **Evaluation:** a rubric (factual accuracy, citation accuracy, completeness, source quality) scored by an LLM judge plus human spot checks; cost and time per task.

## ✅ Takeaways
Orchestrator-worker with **parallel specialists**, condensed context hand-offs, durable workflows, budgets, citation verification. Tell it as **your** story.
