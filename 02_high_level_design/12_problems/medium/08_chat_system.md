# 🟡 08. Chat System (WhatsApp / Messenger / Slack)

📖 Related: primer [Communication](https://github.com/donnemartin/system-design-primer#communication) · [How Discord stores trillions of messages](https://discord.com/blog/how-discord-stores-trillions-of-messages) · [Slack architecture (primer list)](https://github.com/donnemartin/system-design-primer#real-world-architectures)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** 1:1 and group chat (≤ 500 members), online/offline presence, delivered/read receipts, message history across devices, push notifications when offline, media (stretch goal).
**Non-functional:** low latency (< 100 ms delivery), **messages never lost**, ordering within a conversation, high availability.

## 2. Estimates
50M daily active users × 40 messages/day = 2B messages/day → ~25K msgs/s. At 100 B each → 200 GB/day.
Concurrent connections: about 10M+ WebSockets → ~100K connections per server → **100+ chat servers**.

## 3. Connection choice
**WebSockets** (bidirectional, persistent). Fallback: long polling. Stateless HTTP services handle login, profile, and history.

## 4. High-level design
```
Client ⇄ WebSocket ⇄ Chat server (stateful, holds connections)
                         │ 1. persist
                         ▼
                   Message store (Cassandra: PK conversation_id, CK message_id)
                         │ 2. route
                         ▼
        Session registry (Redis: user_id → chat_server_id)
                         │
         recipient online? ── yes → forward to their chat server (via pub/sub or direct RPC)
                         └── no  → Push notification service (APNs/FCM)
Presence service (heartbeats → Redis with TTL)    Media → S3 + CDN
Service discovery (ZooKeeper) assigns clients to the least-loaded chat server
```

## 5. Deep dives
- **Message IDs and ordering:** per-conversation monotonic IDs (Snowflake, or a sequence per conversation). The client orders by ID. Server timestamps beat client timestamps.
- **Delivery guarantees:** client sends with a client-generated `msg_uuid` (dedup) → server persists, then ACKs "sent" → recipient ACKs "delivered" → "read". Retry until ACKed = **at-least-once + dedup**.
- **Offline sync:** each device stores its `last_seen_message_id` and pulls everything after it on reconnect.
- **Group chat:** small groups → fan out to each member's inbox on write. Huge channels (Slack/Discord) → fan out on read.
- **Presence:** heartbeat every ~30 s. If it's missed, the user is offline (Redis TTL). Publish changes only to friends who are online. Throttle to avoid presence storms.
- **Storage:** Cassandra or HBase. Write-heavy, time-ordered reads per conversation, so partition by `conversation_id` (bucketed by time for huge chats).
- **End-to-end encryption:** Signal protocol. The server only sees ciphertext.

## ✅ Takeaways
WebSockets + a **session registry** + persist-then-deliver + ACKs with client dedup IDs + Cassandra partitioned by conversation.
LLD version: [online_chat.py](../../../03_low_level_design/problems/online_chat.py).

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How does a message get delivered from user A to user B?</b></summary>

A sends over a **WebSocket** to its chat server → the server **persists** the message (Cassandra) → looks up B's connection in the **session registry** (Redis: user → server) → forwards it to B's chat server → which pushes it over B's WebSocket. If B is offline, send a push notification; B syncs when it reconnects.

</details>

<details>
<summary><b>Q2. How do you guarantee message ordering?</b></summary>

Within a conversation, assign **monotonically increasing message IDs** on the server (Snowflake or a per-conversation sequence) and order by ID on the client. Don't trust client clocks. Ordering across different conversations isn't needed.

</details>

<details>
<summary><b>Q3. How do you make sure messages aren't lost or duplicated?</b></summary>

The client attaches a **client-generated message ID**. The server persists before acknowledging ("sent"), and the client retries until it gets the ack (**at-least-once**). The server **dedupes** by the client message ID. Delivery and read receipts are separate acks.

</details>

<details>
<summary><b>Q4. How is online presence implemented?</b></summary>

Clients send a **heartbeat** every ~30 s. Presence is stored in Redis with a TTL, so a missed heartbeat means offline. Publish presence changes only to the user's contacts who are online, and throttle updates to avoid storms.

</details>

<details>
<summary><b>Q5. Why Cassandra for messages instead of Postgres?</b></summary>

The workload is **write-heavy and enormous**, and reads are almost always "latest N messages of conversation X". Cassandra's partition key (conversation_id) + clustering key (message_id) fits that pattern, with linear write scalability and multi-datacenter replication.

</details>
