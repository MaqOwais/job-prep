# 🧠 CS Fundamentals (the "SWE fundamentals" round)

Many SWE loops include rapid-fire questions on OS, networking, databases, concurrency, and OOP, either as their own round or mixed into coding and design. Each file gives you **the answer you'd say out loud in 30–60 seconds**.

| # | Topic | Key questions covered |
|---|---|---|
| 1 | [Operating systems](01_operating_systems.md) | Process vs thread, scheduling, memory and paging, deadlock, file systems |
| 2 | [Networking](02_networking.md) | OSI, TCP handshake, what happens when you type a URL, DNS, TLS, HTTP versions |
| 3 | [Databases & SQL](03_databases_sql.md) | ACID, isolation levels, indexes, joins, normalization, **SQL query practice** |
| 4 | [Concurrency](04_concurrency.md) | Race conditions, locks, semaphores, producer-consumer, Python GIL, async |
| 5 | [OOP](05_oop.md) | 4 pillars, composition vs inheritance, interfaces, SOLID |

Also see: [System design concepts](../02_high_level_design/) · [LLD](../03_low_level_design/)

---

## ⚡ Rapid-fire quiz
Cover the answers and test yourself. Aim for a crisp 1–2 sentence answer to each.

| # | Question | Short answer |
|---|---|---|
| 1 | Process vs thread? | A process has its own memory space. Threads share their process's memory, so they're cheaper to create and switch, but need synchronization. |
| 2 | What is a deadlock? 4 conditions? | Two or more threads each waiting on the other forever. Mutual exclusion, hold and wait, no preemption, circular wait. |
| 3 | Mutex vs semaphore? | A mutex lets one owner in at a time. A semaphore is a counter allowing N concurrent holders. |
| 4 | Virtual memory? | Each process sees its own address space, mapped to physical memory through page tables. Enables isolation and swapping. |
| 5 | Stack vs heap? | Stack: per-thread, automatic, fast, for function frames. Heap: shared, dynamic allocation, garbage-collected or managed manually. |
| 6 | TCP vs UDP? | TCP is reliable and ordered, with a connection. UDP is fast, connectionless, and best effort. |
| 7 | TCP 3-way handshake? | SYN → SYN-ACK → ACK. |
| 8 | What does DNS do? | Resolves names to IPs through a cached hierarchical lookup. |
| 9 | HTTPS? | HTTP over TLS. A certificate proves the server's identity; asymmetric key exchange sets up symmetric session keys. |
| 10 | HTTP/1.1 vs 2 vs 3? | 1.1: keep-alive, one request at a time per connection. 2: multiplexed binary frames over one TCP connection. 3: QUIC over UDP, no TCP head-of-line blocking. |
| 11 | ACID? | Atomicity, Consistency, Isolation, Durability. |
| 12 | What does an index do? | A B-tree (usually) that speeds up lookups and range scans, at the cost of slower writes and extra storage. |
| 13 | Clustered vs non-clustered index? | Clustered: table rows are physically ordered by the key (one per table). Non-clustered: a separate structure pointing to the rows. |
| 14 | Normalization? | Removing redundancy (1NF → 2NF → 3NF). Denormalize to speed up reads. |
| 15 | Optimistic vs pessimistic locking? | Optimistic: check a version on write, retry on conflict. Pessimistic: lock the row up front. |
| 16 | What is the GIL? | CPython's global interpreter lock lets only one thread run Python bytecode at a time. Use multiprocessing for CPU-bound work and threads/asyncio for I/O-bound work. (Python 3.13+ offers an experimental free-threaded build.) |
| 17 | Concurrency vs parallelism? | Concurrency is dealing with many tasks at once (interleaving). Parallelism is doing many at the same instant (multiple cores). |
| 18 | Polymorphism? | The same interface with different implementations, resolved at runtime (overriding) or compile time (overloading). |
| 19 | Composition vs inheritance? | Composition = "has-a", flexible, preferred. Inheritance = "is-a", tight coupling. |
| 20 | What is a race condition? | The result depends on the timing of concurrent operations on shared state, e.g. `count += 1` from two threads. |
| 21 | What happens when you type google.com? | DNS → TCP → TLS → HTTP request → LB/servers → response → render ([full answer](02_networking.md#what-happens-when-you-type-googlecom)). |
| 22 | Context switch? | The OS saves one thread's registers and state and loads another's. It has a cost, which is why there's thread-pool sizing. |
| 23 | Paging vs segmentation? | Paging uses fixed-size blocks (no external fragmentation). Segmentation uses variable logical segments. |
| 24 | Garbage collection? | Automatic memory reclamation: reference counting (+ cycle detector in Python), mark-and-sweep, generational. |
| 25 | REST idempotent methods? | GET, PUT, DELETE (and HEAD, OPTIONS). POST isn't idempotent. |
