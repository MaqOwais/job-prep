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
