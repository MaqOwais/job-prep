# 🟢 05. Unique ID Generator in a Distributed System

📖 Related: [Twitter Snowflake (original repo)](https://github.com/twitter-archive/snowflake) · [Instagram: sharding & IDs](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)
⏱️ Try it yourself first: 25 minutes.

## 1. Requirements
IDs must be **unique**, roughly **sortable by time**, 64-bit numeric, generated at 10K+/s, and highly available (no central bottleneck).

## 2. Options
| Approach | Pros | Cons |
|---|---|---|
| DB auto-increment | Simple | Single point of failure, doesn't scale; multi-master with step N is awkward |
| UUID v4 (128-bit random) | No coordination | 128 bits, not sortable, poor B-tree index locality |
| UUID v7 / ULID | Time-ordered, no coordination | 128 bits |
| Ticket server (Flickr) | Simple, numeric | Ticket server is a SPOF unless there are 2+ (odd/even) |
| **Snowflake** ✓ | 64-bit, time-sortable, no coordination at runtime | Depends on clock sync; worker IDs need assigning |

## 3. Snowflake layout (64 bits)
```
| 1 bit sign | 41 bits timestamp (ms since custom epoch) | 5 bits datacenter | 5 bits machine | 12 bits sequence |
```
- 41 bits of ms ≈ **69 years**.
- 12-bit sequence = **4,096 IDs per ms per machine**.
- 1,024 machines (5 + 5 bits).

```python
import time, threading
class Snowflake:
    EPOCH = 1_700_000_000_000
    def __init__(self, dc, machine):
        self.dc, self.machine, self.seq, self.last = dc, machine, 0, -1
        self.lock = threading.Lock()
    def next_id(self):
        with self.lock:
            now = int(time.time() * 1000)
            if now < self.last: raise RuntimeError("clock moved backwards")
            if now == self.last:
                self.seq = (self.seq + 1) & 0xFFF
                if self.seq == 0:                      # exhausted this ms → wait
                    while now <= self.last: now = int(time.time() * 1000)
            else:
                self.seq = 0
            self.last = now
            return ((now - self.EPOCH) << 22) | (self.dc << 17) | (self.machine << 12) | self.seq
```

## 4. Deep dives
- **Clock skew / NTP moving the clock backwards:** refuse to generate IDs, or wait until the clock passes the last timestamp.
- **Assigning machine IDs:** ZooKeeper/etcd, or from config at deploy time.
- **Sortable IDs** let you use them as cursor-pagination keys and as Cassandra clustering keys.

## ✅ Takeaways
Snowflake bit layout + clock-skew handling. These IDs show up in **every** other design (tweets, messages, orders).

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Explain the Snowflake ID layout.</b></summary>

64 bits: **1 sign bit + 41 bits of millisecond timestamp** (since a custom epoch, ~69 years) **+ 10 bits of machine ID** (often 5 datacenter + 5 worker) **+ 12 bits of sequence** (4,096 IDs per ms per machine). IDs are unique without coordination and roughly time-sortable.

</details>

<details>
<summary><b>Q2. What happens if the system clock moves backwards?</b></summary>

IDs could repeat or go out of order. Detect it (current time < last timestamp) and **refuse to generate** IDs until the clock catches up, or wait/sleep for short skews. For large skews, alert and take the node out of rotation. Use NTP with slewing instead of jumps.

</details>

<details>
<summary><b>Q3. Why not just use UUIDv4?</b></summary>

It's 128 bits (bigger indexes and keys), **not sortable** by time, and random inserts scatter across B-tree pages (poor locality, slower writes). It's fine when you just need uniqueness. Time-ordered options like UUIDv7/ULID or Snowflake are better for primary keys.

</details>

<details>
<summary><b>Q4. How are machine IDs assigned?</b></summary>

From **ZooKeeper/etcd** (lease-based registration), deployment configuration, or derived from something unique like a pod ordinal. They must be unique among live generators, or two nodes could emit the same IDs.

</details>

<details>
<summary><b>Q5. Why are time-sortable IDs useful elsewhere in a design?</b></summary>

They make good **cursor pagination** keys, Cassandra **clustering keys** (time order for free), and help with debugging (you can read the creation time from the ID). They also let you shard and order without a separate timestamp index.

</details>
