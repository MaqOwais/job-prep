# 1. Operating Systems

📖 Deeper: [OSTEP: Operating Systems: Three Easy Pieces (free book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)

## Processes and threads
| | Process | Thread |
|---|---|---|
| Memory | Own address space | Shares the process's memory (heap, globals); own stack and registers |
| Creation cost | High (fork/exec) | Low |
| Communication | IPC: pipes, sockets, shared memory, message queues | Shared variables (needs locks) |
| Crash isolation | One crash doesn't kill others | One thread crashing can kill the whole process |

**Process states:** New → Ready → Running → Waiting (blocked on I/O) → Terminated.
**Context switch:** save the PCB (registers, PC, stack pointer), load another. It's pure overhead, and switching processes is more expensive than switching threads because of TLB/cache flushes.
**User vs kernel mode:** system calls (`read`, `write`, `fork`) switch into kernel mode.

## CPU scheduling
FCFS · Shortest Job First · **Round robin** (time slices) · Priority (risk of starvation → aging) · Multilevel feedback queue (what real OSes use, e.g. Linux CFS is fairness-based).

## Memory
- **Virtual memory:** each process gets a private address space. The **MMU** translates virtual addresses to physical ones using **page tables**, with the **TLB** caching translations.
- **Paging:** fixed-size pages (4 KB). A **page fault** happens when the page isn't in RAM, so it's loaded from disk (swap).
- **Thrashing:** constant page faults when the working set doesn't fit in RAM.
- Page replacement policies: LRU, FIFO, Clock.
- **Stack** (function frames, local variables, per thread) vs **heap** (dynamic allocation).
- Memory leaks, fragmentation (internal vs external).

## Synchronization and deadlock
**Deadlock** requires all four conditions (Coffman): mutual exclusion, hold and wait, no preemption, **circular wait**.
Prevention: break one of them. Most commonly, **acquire locks in a global order**, or use timeouts/`try_lock`.
Other approaches: avoidance (Banker's algorithm) and detection plus recovery.
**Livelock** (threads keep reacting to each other without progress) · **Starvation** (a thread never gets a resource).
See [Concurrency](04_concurrency.md) for locks and semaphores.

## File systems and I/O
- Inodes (metadata + block pointers), directories map names to inodes, hard links vs symbolic links.
- Journaling (ext4) for crash consistency.
- **Blocking vs non-blocking I/O**, **epoll/kqueue** (how NGINX and Node handle thousands of connections), memory-mapped files, zero-copy (`sendfile`).
- Page cache: the OS caches disk blocks in RAM.

## Linux commands worth knowing
`ps aux`, `top/htop`, `kill -9`, `lsof`, `strace`, `df -h`, `du -sh`, `free -m`, `netstat -tulpn`/`ss`, `grep`, `awk`, `tail -f`, `chmod 755`, `nohup`, `&`, `systemctl`, `journalctl`.

## Interview questions
1. Process vs thread. When would you use multiprocessing instead of threads? (CPU-bound work in Python because of the GIL; isolation.)
2. What happens during a context switch?
3. Explain virtual memory and a page fault.
4. Four deadlock conditions and how to prevent deadlock.
5. How does a web server handle 10K concurrent connections? (Event loop + epoll, not one thread per connection.)
6. What does `fork()` return? (0 in the child, the child's PID in the parent; copy-on-write.)

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Process vs thread: what's the difference, and when would you use multiple processes instead of threads?</b></summary>

A process has its **own address space**. Threads share their process's memory but have their own stack and registers. Use processes for **isolation** (one crash doesn't kill the others), security boundaries, and **CPU-bound Python** (bypassing the GIL). Use threads for lightweight concurrency with shared state, and I/O-bound work.

</details>

<details>
<summary><b>Q2. What happens during a context switch, and why is it expensive?</b></summary>

The OS saves the current thread's registers, program counter, and stack pointer (in its control block), picks the next thread, and restores its state. It's pure overhead, and switching **processes** also changes the address space, which can flush the **TLB** and pollute the CPU caches.

</details>

<details>
<summary><b>Q3. Explain virtual memory and a page fault.</b></summary>

Each process sees a private **virtual address space**. The MMU translates addresses through **page tables** (cached in the TLB). If a page isn't in RAM, a **page fault** occurs and the OS loads it from disk (swap or file) and updates the table. That enables isolation, overcommitting memory, and memory-mapped files.

</details>

<details>
<summary><b>Q4. What are the four conditions for deadlock, and how do you prevent it?</b></summary>

**Mutual exclusion, hold and wait, no preemption, circular wait.** Break any one. Most practical: **acquire locks in a consistent global order** (breaks circular wait), use timeouts / try-lock and back off, or acquire all needed locks at once.

</details>

<details>
<summary><b>Q5. How can one server handle 10,000 concurrent connections?</b></summary>

Not with one thread per connection (memory and context-switch overhead). Use **non-blocking I/O with an event loop** (epoll on Linux, kqueue on macOS) that watches many sockets and processes only the ready ones. That's how NGINX, Node.js, and Python asyncio work. Pair it with a small worker pool for CPU-heavy tasks.

</details>
