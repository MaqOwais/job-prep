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
