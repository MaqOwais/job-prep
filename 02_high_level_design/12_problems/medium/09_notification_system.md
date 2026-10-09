# 🟡 09. Notification System (Push, SMS, Email)

📖 Related: primer [Asynchronism](https://github.com/donnemartin/system-design-primer#asynchronism) · [Message queues](https://github.com/donnemartin/system-design-primer#message-queues)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** send notifications through push (iOS/Android), SMS, and email; triggered by services or scheduled; user preferences and opt-out; templates; delivery tracking.
**Non-functional:** 10M+ notifications/day, soft real-time (seconds), **no duplicates**, no lost notifications, rate limits per user (don't spam people).

## 2. High-level design
```
Services / Scheduler → Notification API (auth, validate, rate limit)
                         │
                         ├─ User prefs + device tokens (DB + cache)
                         ├─ Template service (render the message)
                         ▼
                Kafka topics: push | sms | email   (one queue per channel → isolation)
                         ▼
          Channel workers ──→ 3rd-party providers: APNs, FCM, Twilio, SES/SendGrid
                 │ fail → retry with backoff → DLQ
                 ▼
          Notification log (status: queued/sent/delivered/opened) → analytics
```

## 3. Deep dives
- **Why one queue per channel?** If the SMS provider is down, push and email keep flowing (the bulkhead pattern).
- **Reliability:** persist the notification before enqueueing it. At-least-once delivery + **dedup by notification_id** in workers.
- **Retries:** exponential backoff, a DLQ after N attempts, provider failover (Twilio → a backup provider).
- **User experience:** respect preferences and quiet hours, cap frequency (e.g. ≤ 3 marketing pushes/day), batch digests.
- **Priority:** OTPs and security alerts on a high-priority queue; marketing on a low-priority one.
- **Scheduling:** a scheduler service polls due jobs, or uses delayed queues.
- **Tracking:** provider callbacks/webhooks update the delivery status; open/click tracking via links and pixels.
- **Security:** only authenticated internal services can call the API. Keep device tokens private.

## ✅ Takeaways
Separate queue per channel, dedup + retries + DLQ, user preferences and rate limits, provider abstraction with failover.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why use a separate queue per channel (push, SMS, email)?</b></summary>

**Isolation (bulkheads):** if the SMS provider is slow or down, its backlog doesn't delay push or email. Each channel also scales its workers independently and has its own retry policy and rate limits.

</details>

<details>
<summary><b>Q2. How do you avoid sending duplicate notifications?</b></summary>

Give each notification a unique **notification_id** (or an idempotency key from the caller). Workers check a dedup store (Redis SET with a TTL) before sending, because queues deliver at least once.

</details>

<details>
<summary><b>Q3. What happens when a third-party provider (e.g., Twilio) fails?</b></summary>

Retry with **exponential backoff and jitter**, open a circuit breaker if it keeps failing, **fail over to a secondary provider**, and move permanently failing messages to a DLQ. Track delivery status from provider callbacks.

</details>

<details>
<summary><b>Q4. How do you respect user preferences and avoid spamming people?</b></summary>

Check per-user **opt-in/opt-out** settings by channel and category, quiet hours with time zones, and **frequency caps** (e.g., max 3 marketing pushes/day). Batch low-priority items into digests. Critical messages (OTP, security alerts) bypass marketing limits.

</details>

<details>
<summary><b>Q5. How do you prioritize an OTP over a marketing blast?</b></summary>

Separate **priority queues** (or topics) with dedicated worker capacity for high-priority traffic, so a million-message campaign can't delay one-time passwords. Rate-limit marketing sends.

</details>
