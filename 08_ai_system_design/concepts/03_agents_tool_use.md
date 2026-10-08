# 3. Agents & Tool Use

📖 Must-read: [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) · [Model Context Protocol](https://modelcontextprotocol.io/)

> 💡 This is your strongest topic. Your research built **orchestrator, router, analyst, configuration/creation, manager, and skill-based data-fetching agents**. Map every concept below to something you actually built.

## Workflow vs agent
- **Workflow:** LLM calls wired together in **predefined code paths** (chains, routing, parallelization). Predictable, cheaper, easier to test.
- **Agent:** the **LLM decides** which tools to call and when to stop, in a loop. Flexible but less predictable.
> "Use the simplest pattern that works. Reach for an agent only when the steps can't be known in advance."

## Common patterns
| Pattern | What | Example |
|---|---|---|
| Prompt chaining | Step 1 output → step 2 input, with checks between steps | Outline → draft → edit |
| **Routing** | A classifier or LLM sends the input to a specialized handler or model | Support ticket → billing / technical / refund agent; cheap vs expensive model |
| Parallelization | Run subtasks in parallel and aggregate (sectioning or voting) | Check code with 3 reviewers |
| **Orchestrator-workers** | An orchestrator LLM breaks down the task and delegates to workers, then synthesizes | Research assistant ([problem 08](../problems/medium/08_multi_agent_research_assistant.md)) |
| Evaluator-optimizer | One LLM generates, another critiques, and it loops | Translation, code fixing |
| **Autonomous agent** | Loop: think → act (tool call) → observe → repeat until done | Coding agents, computer use |

## The agent loop
```
while not done and steps < MAX_STEPS:
    response = llm(system_prompt, history, tool_schemas)
    if response.tool_calls:
        for call in response.tool_calls:
            result = execute_tool(call)          # sandboxed, with timeouts and permissions
            history.append(tool_result(call, result))
    else:
        done = True                               # final answer
```
**ReAct** = interleaved reasoning + acting. Modern models do this natively through tool-calling APIs.

## Tools
- Defined with a **name, description, and JSON schema** for parameters. **Good tool descriptions matter as much as prompts.**
- **MCP (Model Context Protocol):** an open standard for exposing tools, resources, and prompts to any compatible agent or client. "USB-C for AI tools." Mention it when designing tool integrations.
- Agent-to-agent protocols (e.g., A2A) for cross-vendor agent communication.
- Tool design: idempotent where possible, clear errors the LLM can recover from, paginated outputs (don't flood the context).

## Memory
| Type | Implementation |
|---|---|
| Short-term (this conversation) | Message history; **summarize or trim** when it's near the context limit |
| Long-term (across sessions) | Store facts and preferences → retrieve with vector search or key-value lookup |
| Episodic / task state | A durable store (DynamoDB/Postgres) so long tasks survive crashes |

## Multi-agent systems
- **Orchestrator / supervisor** delegates to specialist agents (your Manager and Router agents).
- **Pros:** separation of concerns, smaller focused prompts, parallelism, different models per agent.
- **Cons:** more tokens and latency, error compounding, harder debugging. Use only when the task truly splits.
- Communication: a shared state object or blackboard, message passing, or tool calls between agents.

## Production concerns (what separates senior answers)
- **Step limits, timeouts, budget caps** (tokens and $ per task).
- **Human-in-the-loop** approval for irreversible actions (payments, emails, deleting data).
- **Least-privilege tools:** an agent's permissions = the user's permissions, never more.
- **Sandboxing** for code execution (containers / Firecracker microVMs).
- **Durable execution:** checkpoint the state so long-running agents can resume (Step Functions, Temporal).
- **Tracing every step** (inputs, tool calls, outputs, tokens) for debugging and evaluation.
- **Prompt-injection defense:** tool outputs and documents are **untrusted data** (see [safety](06_safety_security.md)).

## ✅ Self-check
- [ ] Workflow vs agent: when would you use each?
- [ ] Draw the orchestrator-worker pattern using your own research project
- [ ] How do you stop an agent from looping forever or overspending?
- [ ] What is MCP and why does it matter?
