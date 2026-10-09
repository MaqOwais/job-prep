# 🟢 01. Customer Support Chatbot

📖 Concepts: [LLM fundamentals](../../concepts/01_llm_fundamentals.md) · [Agents & tool use](../../concepts/03_agents_tool_use.md) · [Safety](../../concepts/06_safety_security.md)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** answer customer questions about orders, returns, and policies; look up order status (tool call); hand off to a human agent when needed; remember the conversation.
**Non-functional:** responds in < 2 s to first token, available 24/7, never invents policies, protects customer data. **Success metric: deflection rate** (resolved without a human) with good CSAT.

## 2. Estimates
50K conversations/day × 6 turns × (1.5K input + 200 output tokens) → about 450M input tokens/day. Use a **mid-size model**; route only hard cases to a larger one.

## 3. High-level design
```
Web/app chat widget ⇄ WebSocket/SSE ⇄ Chat API (auth: logged-in customer ID)
   → Conversation store (DynamoDB: session_id → messages, summary)
   → Orchestrator:
        1. intent router (small model / classifier): FAQ | order_status | refund | complaint | other
        2. FAQ/policy → RAG over the help center (see 05_enterprise_rag_platform)
        3. order_status/refund → tool calls to the Orders API (scoped to THIS customer's ID only)
        4. low confidence / angry sentiment / "talk to a human" → handoff to the agent queue with a summary
   → LLM (streamed) → output guardrails → client
Feedback (👍/👎, CSAT) + transcripts → eval pipeline
```

## 4. Deep dives
- **Memory:** keep the last N turns plus a running **summary** to stay within the context window.
- **Tools must be scoped:** the order lookup tool takes the customer ID **from the auth session**, never from the model's arguments. This prevents someone asking about other people's orders.
- **Handoff:** pass the human agent a summary, the detected intent, and the steps already tried, so the customer doesn't repeat themselves.
- **No invented policies:** answer only from retrieved policy text, cite it, and say "I'm not sure, let me connect you" when retrieval confidence is low.
- **Refunds:** the LLM proposes; business rules or a human approve above a threshold.
- **Evaluation:** a golden set of real tickets; metrics are deflection, CSAT, escalation precision, and policy accuracy.

## ✅ Takeaways
Router → RAG for knowledge + **scoped tools** for actions → human handoff. Memory via summaries. Measure deflection *and* quality.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do you stop the bot from inventing refund policies?</b></summary>

Answer only from **retrieved policy documents** (RAG) with citations, instruct it to refuse or escalate when the context doesn't cover the question, add a groundedness check on the output, and let business rules (not the LLM) decide refunds above a threshold.

</details>

<details>
<summary><b>Q2. How do you prevent one customer from seeing another customer's orders?</b></summary>

The order-lookup tool takes the customer ID **from the authenticated session**, never from model-generated arguments. The tool enforces authorization server-side, so even a prompt-injected request can only see the logged-in user's data.

</details>

<details>
<summary><b>Q3. When and how should the bot hand off to a human?</b></summary>

Trigger on low confidence, repeated failures, negative sentiment, sensitive topics, or an explicit request. Pass the agent a **summary**, the detected intent, the customer's details, and the steps already tried, so the customer doesn't have to repeat everything.

</details>

<details>
<summary><b>Q4. How do you keep long conversations within the context window?</b></summary>

Keep the last N turns verbatim plus a **rolling summary** of earlier turns, store key facts (order number, issue) in structured session state, and retrieve only the knowledge relevant to the current question.

</details>

<details>
<summary><b>Q5. Which metrics define success?</b></summary>

**Deflection/resolution rate** without a human, CSAT, escalation precision (escalated when it should be), policy accuracy on a golden test set, average handle time, and cost per conversation.

</details>
