# 🟢 02. Rate Limiter

📖 Related: primer [Back pressure](https://github.com/donnemartin/system-design-primer#back-pressure) · [Stripe: Rate limiters](https://stripe.com/blog/rate-limiters) · [Cloudflare: counting things at scale](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** limit requests per client (user ID, IP, or API key) per rule (e.g. 100 requests/min). Return **HTTP 429** with a `Retry-After` header when over the limit.
**Non-functional:** very low added latency (< 1–2 ms), distributed across many API servers, accurate enough, fault tolerant (**fail open** if the limiter itself goes down).

## 2. Where does it live?
Client side (can't be trusted) ✗ · **API gateway / middleware** ✓ (most common) · inside each service.

## 3. Algorithms (know all 5, implement 2)
| Algorithm | How | Pros | Cons |
|---|---|---|---|
| **Token bucket** | A bucket holds up to B tokens and refills at R/s; each request takes one token | Allows bursts, memory-efficient, the most popular choice (AWS, Stripe) | Two parameters to tune |
| Leaky bucket | A FIFO queue drains at a fixed rate | Smooth output | Bursts fill the queue; old requests block new ones |
| **Fixed window counter** | Count per window (`user:12:00`) | Simple, cheap | Spike at window edges (up to 2× the limit) |
| Sliding window log | Store a timestamp per request; count those in the last 60 s | Exact | Memory-heavy |
| **Sliding window counter** | `current + previous × overlap%` | Accurate enough, cheap | An approximation |

```python
import time
class TokenBucket:
    def __init__(self, capacity, refill_per_sec):
        self.cap, self.rate = capacity, refill_per_sec
        self.tokens, self.last = capacity, time.monotonic()
    def allow(self):
        now = time.monotonic()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1; return True
        return False
```

## 4. Distributed design
```
Client → LB → API Gateway (rate-limit middleware) ──→ Redis cluster (counters/tokens)
                       │ allowed                        ▲
                       ▼                                │ rules cached locally
                   Services                      Rules config (YAML/DB)
```
- State lives in **Redis** (fast, with TTLs). Use a **Lua script** or `INCR` + `EXPIRE` so the check-and-update is **atomic**. That avoids race conditions between gateway nodes.
- Key: `rl:{rule}:{client_id}:{window}`.
- Rules are cached in memory on each gateway and refreshed periodically.
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.

## 5. Deep dives
- **Race conditions:** read-then-write isn't atomic, so use Lua or `INCR`.
- **Latency:** Redis is about 1 ms. An alternative is local counters synced asynchronously, which is less accurate.
- **Multi-region:** per-region limits, or eventually consistent global counters.
- **Fail open vs fail closed:** usually fail open, since availability matters more than strict limits. For an auth/login limiter, fail closed.
- Hard vs soft limits; tiered limits per plan; dropping vs queueing excess requests.

## ✅ Takeaways
Token bucket + Redis + Lua for atomicity + 429 responses. Discuss **fail-open** behavior and **edge bursts** in fixed windows.
Related LLD: implementing this class cleanly is a common coding/LLD question too.
