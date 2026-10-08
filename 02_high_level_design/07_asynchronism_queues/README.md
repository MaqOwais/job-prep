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
