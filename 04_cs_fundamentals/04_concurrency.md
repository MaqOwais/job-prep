# 4. Concurrency

📖 Practice: [LeetCode Concurrency problems](https://leetcode.com/problemset/concurrency/) · *Java Concurrency in Practice* (classic)

## Core vocabulary
- **Race condition:** the outcome depends on thread timing. `count += 1` is really read → add → write, which isn't atomic.
- **Critical section:** code that touches shared state. Protect it.
- **Atomic operation:** happens all at once (CAS, `AtomicInteger`).
- **Deadlock / livelock / starvation:** see [OS](01_operating_systems.md#synchronization-and-deadlock).
- **Thread-safe:** works correctly under concurrent access.

## Synchronization primitives
| Primitive | What | Use |
|---|---|---|
| **Mutex / Lock** | One holder at a time | Protect shared state |
| **RLock (reentrant)** | The same thread can acquire it again | Recursive code |
| **Semaphore(n)** | Up to n holders | Connection pools, rate limiting |
| **Condition variable** | Wait until notified | Producer-consumer |
| **Read-write lock** | Many readers OR one writer | Read-heavy caches |
| **CAS (compare-and-swap)** | Lock-free atomic update | Counters, lock-free structures |
| **Barrier / latch** | Wait until N threads arrive | Phased computation |

## Classic problem: producer-consumer (bounded buffer)
```python
import threading, queue

q = queue.Queue(maxsize=10)     # thread-safe, blocks when full/empty

def producer():
    for i in range(100):
        q.put(i)                # blocks if full → back pressure
    q.put(None)                 # sentinel

def consumer():
    while (item := q.get()) is not None:
        process(item)

# Manual version with Condition
class BoundedBuffer:
    def __init__(self, cap):
        self.buf, self.cap = [], cap
        self.cv = threading.Condition()
    def put(self, x):
        with self.cv:
            while len(self.buf) >= self.cap: self.cv.wait()   # always `while`, not `if` (spurious wakeups)
            self.buf.append(x); self.cv.notify_all()
    def get(self):
        with self.cv:
            while not self.buf: self.cv.wait()
            x = self.buf.pop(0); self.cv.notify_all(); return x
```

## Thread-safe counter and singleton
```python
class Counter:
    def __init__(self): self.n, self.lock = 0, threading.Lock()
    def inc(self):
        with self.lock: self.n += 1

class Singleton:                       # double-checked locking
    _inst, _lock = None, threading.Lock()
    @classmethod
    def get(cls):
        if cls._inst is None:
            with cls._lock:
                if cls._inst is None: cls._inst = cls()
        return cls._inst
```

## Python specifics
- **GIL:** only one thread runs Python bytecode at a time (in standard CPython builds).
  - **I/O-bound** (network, disk) → `threading` or **`asyncio`** (the GIL is released during I/O).
  - **CPU-bound** → `multiprocessing` / `ProcessPoolExecutor` (separate processes, separate GILs) or native libraries (NumPy releases the GIL).
- `concurrent.futures.ThreadPoolExecutor` / `ProcessPoolExecutor` are the easy high-level APIs.
- `asyncio`: a single-threaded event loop with cooperative multitasking (`async`/`await`). Great for thousands of sockets.

## Java specifics (since your resume lists Java)
`synchronized`, `volatile` (visibility, not atomicity), `ReentrantLock`, `ConcurrentHashMap`, `AtomicInteger`, `ExecutorService`, `CompletableFuture`, `CountDownLatch`.

## Classic interview problems
| Level | Problem |
|---|---|
| 🟢 | [Print in Order](https://leetcode.com/problems/print-in-order/) |
| 🟡 | [Print FooBar Alternately](https://leetcode.com/problems/print-foobar-alternately/) · [Print Zero Even Odd](https://leetcode.com/problems/print-zero-even-odd/) · [Building H2O](https://leetcode.com/problems/building-h2o/) · [Design Bounded Blocking Queue](https://leetcode.com/problems/design-bounded-blocking-queue/) (🔒) |
| 🔴 | [The Dining Philosophers](https://leetcode.com/problems/the-dining-philosophers/) · [Web Crawler Multithreaded](https://leetcode.com/problems/web-crawler-multithreaded/) (🔒) |

## Interview questions
1. What's a race condition, and how do you fix it?
2. Mutex vs semaphore.
3. Why use `while` instead of `if` around `wait()`? (Spurious wakeups, and another thread may have consumed the item.)
4. How would you make a cache thread-safe? (A lock, a read-write lock, or a concurrent map + atomic operations.)
5. Threads vs processes vs asyncio in Python: when would you use each?
6. How do you avoid deadlock with multiple locks? (A global lock ordering.)

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What is a race condition? Give an example and a fix.</b></summary>

The result depends on the timing of concurrent operations on shared state. Example: two threads run count += 1 (read → add → write), and one update is lost. Fix: a **lock/mutex** around the critical section, an **atomic** operation (AtomicInteger, Redis INCR), or avoid shared mutable state (message passing).

</details>

<details>
<summary><b>Q2. Mutex vs semaphore?</b></summary>

A **mutex** lets **one** holder into a critical section and is owned by the thread that locked it. A **semaphore** is a counter that allows up to **N** concurrent holders (e.g., limit 10 DB connections). A binary semaphore resembles a mutex but has no ownership semantics.

</details>

<details>
<summary><b>Q3. Why should you call wait() inside a while loop instead of an if?</b></summary>

**Spurious wakeups** can happen, and another thread may consume the condition between the notify and your thread re-acquiring the lock. Re-checking the condition in a while loop guarantees it's actually true before you proceed.

</details>

<details>
<summary><b>Q4. Threads vs processes vs asyncio in Python: when would you use each?</b></summary>

**asyncio:** many I/O-bound tasks (thousands of sockets) on one thread with cooperative scheduling. **Threads:** I/O-bound work with blocking libraries (the GIL is released during I/O). **Processes (multiprocessing):** **CPU-bound** work, which gets true parallelism across cores because each process has its own GIL.

</details>

<details>
<summary><b>Q5. How would you implement a bounded blocking queue?</b></summary>

A buffer + a lock + two **condition variables** (not_full, not_empty). put() waits while full, appends, and notifies not_empty. get() waits while empty, pops, and notifies not_full. Always wait in a while loop. Python's queue.Queue(maxsize) already does this.

</details>
