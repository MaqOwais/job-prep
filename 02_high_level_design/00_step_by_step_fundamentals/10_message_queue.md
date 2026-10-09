# Step 10 of 13: Message Queue (decoupling + async work)

[🏠 Overview](README.md) · **← Prev** [Step 9](09_multiple_data_centers.md) · **Next →** [Step 11: Logging, metrics, automation](11_logging_metrics_automation.md)

## 📍 Where we are
A multi-data-center, stateless, cached system. All work still happens **inside the request**.

## 🚨 The problem
A user uploads a photo. The server must: save it, create 3 thumbnail sizes, run content moderation, update search, and notify followers. Doing all of that **while the user waits** means:
- **Slow responses** (seconds), and timeouts.
- **Tight coupling:** if the thumbnail service is down, the upload fails.
- **Spikes overwhelm us:** 10× uploads during an event → servers fall over.

## 💡 The fix: a message queue
A message queue is a **durable buffer** between components. **Producers** put messages (tasks or events) in; **consumers (workers)** take them out and process them **asynchronously**.
```
User ──upload──▶ [web server] ──1. save original to S3
                      │        2. publish {"photo_id": 42} ──▶ [ MESSAGE QUEUE ]
                      │                                          │       │
   ◀── "202 Accepted, processing…" (fast!)                       ▼       ▼
                                                        [thumbnail workers] [moderation workers] …
```

## ⚙️ How it works
1. The producer publishes a message and returns immediately. The user gets a fast response.
2. The queue **stores** the message durably until it's processed.
3. Workers pull messages, do the work, and **acknowledge**. If a worker crashes before acknowledging, the message becomes visible again and another worker retries it.
4. After N failed attempts, the message goes to a **dead-letter queue (DLQ)** for inspection.

## 🎁 What we gain
- **Decoupling:** producers and consumers don't need to know about each other or be up at the same time.
- **Independent scaling:** a growing queue → add more workers (autoscale on queue depth).
- **Absorbing spikes:** the queue buffers bursts, and workers drain them at a steady rate.
- **Reliability:** retries + DLQ instead of failed user requests.

## 🔀 Options
| Type | Examples | Use for |
|---|---|---|
| Queue (each message processed once) | SQS, RabbitMQ | Background jobs: emails, thumbnails |
| Pub/sub (fan-out to many subscribers) | SNS, Google Pub/Sub | One event, many reactions |
| Log/stream (replayable, ordered per partition) | **Kafka**, Kinesis | Event streams, analytics, many consumer groups |

## ⚖️ Pitfalls
- **At-least-once delivery:** a message can be processed twice, so **make consumers idempotent** (e.g., "thumbnail for photo 42 already exists → skip").
- **Ordering** is only guaranteed within a partition or FIFO group.
- **Eventual consistency:** the thumbnail appears a few seconds later. Design the UI for that ("processing…").
- More moving parts to monitor (queue depth, consumer lag, DLQ size).

## 🗣️ Say it in an interview
> "The upload API saves the original to S3, publishes an event, and returns 202. Thumbnail and moderation workers consume from the queue, autoscale on queue depth, retry with backoff, and send failures to a DLQ. Consumers are idempotent because delivery is at-least-once."

## 🔗 Go deeper
- [Asynchronism & queues module](../07_asynchronism_queues/) · design problem: [build Kafka](../12_problems/hard/28_distributed_message_queue.md)
- Primer: [Asynchronism](https://github.com/donnemartin/system-design-primer#asynchronism) · [Message queues](https://github.com/donnemartin/system-design-primer#message-queues) · [Back pressure](https://github.com/donnemartin/system-design-primer#back-pressure)

## ✅ Self-check
- [ ] Give 3 problems a queue solves
- [ ] What happens if a worker crashes mid-task?
- [ ] Why must consumers be idempotent?
- [ ] Queue vs pub/sub vs Kafka log

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why would you introduce a message queue between the API and the workers?</b></summary>

To make slow work **asynchronous** (fast responses), **decouple** producers from consumers (they scale and fail independently), **buffer spikes**, and get **retries** for free. Example: the upload API returns 202 while thumbnail workers process the images from the queue.

</details>

<details>
<summary><b>Q2. What happens if a worker crashes halfway through processing a message?</b></summary>

It never acknowledges the message. After the **visibility timeout** (SQS) or session timeout (Kafka consumer group), the message becomes available again and another worker retries it. After N failures it goes to a **dead-letter queue** for investigation.

</details>

<details>
<summary><b>Q3. Why must queue consumers be idempotent?</b></summary>

Most queues guarantee **at-least-once** delivery: retries, timeouts, and rebalances can deliver a message more than once. An idempotent consumer (dedupe by message or business ID, upserts, "already done → skip") makes duplicates harmless.

</details>

<details>
<summary><b>Q4. Queue vs pub/sub vs log (Kafka): what's the difference?</b></summary>

**Queue** (SQS, RabbitMQ): each message is processed by one consumer, then deleted. **Pub/sub** (SNS): each message is copied to all subscribers. **Log** (Kafka, Kinesis): an ordered, retained, **replayable** stream. Multiple consumer groups each read everything at their own offset, with ordering per partition.

</details>

<details>
<summary><b>Q5. How do you know when to scale the workers?</b></summary>

Watch **queue depth / consumer lag** and the age of the oldest message. Autoscale workers on backlog per worker. Also watch the processing error rate and DLQ size. If the queue keeps growing, consumers can't keep up: scale them out, optimize them, or apply back pressure upstream.

</details>

**Next →** [Step 11: Logging, metrics, automation](11_logging_metrics_automation.md)
