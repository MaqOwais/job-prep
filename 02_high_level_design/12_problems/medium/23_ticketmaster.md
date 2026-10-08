# 🟡 23. Ticketmaster (event ticket booking with flash sales)

📖 Related: [Databases: locking](../../05_databases/) · [Payment system](../hard/19_payment_system.md) · [Rate limiter](../easy/02_rate_limiter.md)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** browse and search events; view the seat map; **reserve seats** (held for ~10 minutes while paying); pay and confirm; cancel.
**Non-functional:** **never double-sell a seat** (strong consistency), and survive **huge spikes** (10M users for a 50K-seat concert at 10:00 AM). Browsing can be eventually consistent.

## 2. Core challenge 1: no double booking
Seat states: `AVAILABLE → RESERVED (hold, expires_at) → BOOKED`.
```sql
-- atomic conditional update (optimistic): succeeds for exactly one user
UPDATE seats SET status='RESERVED', user_id=?, expires_at=now()+interval '10 min'
WHERE event_id=? AND seat_id=? AND (status='AVAILABLE' OR (status='RESERVED' AND expires_at < now()));
-- rows_affected = 1 → you got it; 0 → seat taken
```
Alternatives: `SELECT … FOR UPDATE` (pessimistic), or a **Redis lock with a TTL** (`SET seat:{id} user NX EX 600`) in front of the DB for speed, with the DB as the final authority.
**Expired holds:** the conditional update above treats them as available; a sweeper job also cleans them up.

## 3. Core challenge 2: flash-sale traffic
```
Users → CDN (static event pages, seat map images) → LB
     → VIRTUAL WAITING ROOM (queue service): users get a queue position token;
        admitted in batches matching booking capacity (rate-limited admission)
     → Booking service (only admitted tokens) → Seats DB (SQL, partitioned by event_id)
     → Payment service (idempotency key; on success seats → BOOKED; on failure/expiry → AVAILABLE)
Seat availability for display → cache (Redis), refreshed every second (slightly stale is OK)
Search/browse → Elasticsearch (eventually consistent)
```

## 4. Deep dives
- **Waiting room:** protects the booking DB, gives users fairness (first come, first served), and lets you show "you're number 12,345 in line". Tokens are signed so they can't be skipped.
- **Bot protection:** CAPTCHA, per-account limits, device fingerprinting.
- **Hot partition:** one event receives all the traffic. Partition the seats table by event_id, keep the hot event's data in memory, and admit only as many users as the DB can serve.
- **Payment:** reservation and payment form a **saga**. Payment fails or the hold expires → release the seats. Use idempotency keys ([payment system](../hard/19_payment_system.md)).
- **Consistency split:** strong for seat state; eventual for browsing, search, and the seat map cache.

## ✅ Takeaways
**Conditional updates / locks with TTL holds** to prevent double booking + a **virtual waiting room** for spikes + a payment saga with release on failure.
