# 7. Asynchronism & Message Queues

📖 Primer: [Asynchronism](https://github.com/donnemartin/system-design-primer#asynchronism) · [Message queues](https://github.com/donnemartin/system-design-primer#message-queues) · [Task queues](https://github.com/donnemartin/system-design-primer#task-queues) · [Back pressure](https://github.com/donnemartin/system-design-primer#back-pressure)

---

## 7.1 Why go async
- Keep the request path fast: respond "accepted" now, do the heavy work later (video encoding, emails, feed fan-out).
- **Decouple** producers from consumers so they scale and fail independently.
- **Smooth out spikes:** the queue buffers bursts.
- Do expensive work ahead of time (precomputing feeds, for example).

## 7.2 Message queues vs task queues vs streams
| Type | What | Examples |
|---|---|---|
| **Message queue** | Point-to-point. Each message is consumed by one worker, then deleted. | SQS, RabbitMQ |
| **Pub/sub** | One message → many subscribers | SNS, Google Pub/Sub, Redis pub/sub |
| **Log / stream** | Append-only, ordered per partition, **replayable**, consumer groups track offsets | **Kafka**, Kinesis, Pulsar |
| **Task queue** | Queue + scheduled task execution with retries | Celery, Sidekiq |

## 7.3 Key concepts interviewers probe
- **Delivery guarantees:** at-most-once, **at-least-once** (most common, so consumers must be **idempotent**), exactly-once (expensive; Kafka transactions, or dedupe IDs).
- **Ordering:** usually guaranteed only within a partition or a FIFO group. Pick the partition key carefully (e.g. `user_id`).
- **Dead-letter queue (DLQ):** where messages go after N failed attempts.
- **Visibility timeout** (SQS): a message is hidden while being processed and reappears if the worker doesn't acknowledge it.
- **Consumer lag:** a monitoring metric and an autoscaling signal.
- **Fan-out:** SNS → many SQS queues, or Kafka with multiple consumer groups.

## 7.4 Back pressure
When the queue grows faster than workers can drain it: **limit queue size** → reject with HTTP 503 and let clients retry with **exponential backoff + jitter**. This protects the system from collapsing.

## 7.5 Downsides
More moving parts, eventual consistency, harder debugging (use correlation IDs), duplicate messages and ordering issues. For cheap or real-time operations, synchronous calls may be simpler.

## 🗣️ Say it in an interview
> "Uploading returns 202 Accepted immediately. The upload service writes the job to Kafka, partitioned by video_id. Transcoding workers consume it, and failures go to a DLQ after 3 retries. Workers are idempotent on (video_id, resolution), so redelivery is safe."

## ✅ Self-check
- [ ] Queue vs pub/sub vs Kafka log
- [ ] Why does at-least-once delivery require idempotent consumers?
- [ ] How do you keep a single user's events in order?
- [ ] What is back pressure and how do you apply it?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. At-most-once, at-least-once, exactly-once: how is each achieved?</b></summary>

**At-most-once:** acknowledge or commit before processing (may lose messages). **At-least-once:** process, then acknowledge (may duplicate); this is the default. **Exactly-once effect:** at-least-once delivery + **idempotent consumers** (dedupe keys), or transactional processing like Kafka transactions for read-process-write.

</details>

<details>
<summary><b>Q2. How do you guarantee ordering for one user's events?</b></summary>

Use the user ID as the **partition key** (Kafka) or **message group ID** (SQS FIFO). All of that user's events go to one partition, which is consumed in order by one consumer. Global ordering across all events doesn't scale and is rarely needed.

</details>

<details>
<summary><b>Q3. What is a dead-letter queue, and how should you use it?</b></summary>

A queue that receives messages that **failed N times** (poison messages), so they don't block or loop forever. Alert on DLQ growth, inspect and fix the cause, then **redrive** the messages back to the main queue.

</details>

<details>
<summary><b>Q4. What is back pressure?</b></summary>

Signaling producers to slow down when consumers can't keep up: bounded queues, rejecting with 429/503 + Retry-After, rate limiting upstream, or pausing consumption. Without it, queues grow without bound and latency or memory explodes.

</details>

<details>
<summary><b>Q5. When should you NOT make something asynchronous?</b></summary>

When the user needs the result **immediately** to continue (login, payment authorization, reads), the operation is cheap and fast, or the added complexity (eventual consistency, duplicate handling, monitoring) outweighs the benefit.

</details>
