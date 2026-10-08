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

**Next →** [Step 11: Logging, metrics, automation](11_logging_metrics_automation.md)
