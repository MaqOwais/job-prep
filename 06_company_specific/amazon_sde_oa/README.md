# 🟧 Amazon SDE Online Assessment

📖 Related: [Coding patterns](../../01_coding/README.md) · [Behavioral / LPs](../../05_behavioral/README.md) · [Django questions](../../04_cs_fundamentals/06_django.md)

**Deadline:** one week from the invite. Block **2.5–3 hours** in one sitting (the coding timer can't be paused).

| Part | Time | What it is | How it's judged |
|---|---|---|---|
| **1. Coding Challenge** | 100 min, 2 problems | Q1: classic DSA problem (any language). Q2: code-repository task **with an AI coding assistant** (limited language list, can't switch once started) | Hidden test cases pass, code quality, how well you use (and check) the AI |
| **2. Work Simulation** | ~45 min | A simulated day as an Amazon SDE: emails, chats, meetings, data, code/design decisions. You pick or rate responses | Judgement mapped to **Leadership Principles** |
| **3. Work Style Survey** | ~6 min (×2) | Statements about how you like to work | Consistency + fit with LPs |

---

## ✅ Before you start
- [ ] Do the **demo test** from the email at least once, including the code-repository question. Learn the IDE, the run/test buttons, and the AI assistant panel.
- [ ] Latest Chrome or Edge, single monitor, camera uncovered, photo ID ready, stable internet, charger plugged in.
- [ ] Quiet room, phone away, water nearby. Nothing on the desk.
- [ ] Python 3 for Q1 (fastest to write). For Q2 pick the language you **debug** fastest in.
- [ ] It's proctored and you sign an acknowledgement: no outside help, no other tabs. The only AI allowed is the one built into Q2.

---

## 1️⃣ Coding Challenge (100 min)

### Time plan
| Minutes | Do |
|---|---|
| 0–5 | Read **both** problems. Note the language options for Q2. |
| 5–45 | **Q1 (DSA)**: aim to finish in ~40 min |
| 45–95 | **Q2 (repo + AI)** |
| 95–100 | Re-run all tests on both, remove debug prints |

If Q1 stalls at 35 min, submit a brute force that passes some tests and move on. Partial credit beats a blank Q2.

### Q1: classic DSA
Amazon OA problems are usually medium: arrays/strings + hashing, sliding window, two pointers, heaps, greedy + sorting, BFS/graphs, prefix sums, sometimes 1D DP. They're often wrapped in an Amazon story (warehouses, packages, servers, deliveries). Strip the story and find the pattern.

**Routine:**
1. Restate inputs/outputs; write down the constraints. `n ≤ 10^5` → you need O(n log n) or better.
2. Work through the sample by hand.
3. Code the clean version, then test: empty input, single element, all equal, max size, negatives, duplicates.
4. Read the hidden-test failures if shown (timeouts → complexity; wrong answer → edge case).

**High-yield practice (LeetCode, filter tag "Amazon"):** Two Sum, Top K Frequent Elements, Merge Intervals, Number of Islands, Rotting Oranges, K Closest Points, Meeting Rooms II, LRU Cache, Longest Substring Without Repeating Characters, Minimum Window Substring, Course Schedule, Task Scheduler, Partition Labels, Reorganize String, Min Cost to Connect Sticks, Search Suggestions System, Maximum Units on a Truck, Find the Kth Largest, Trapping Rain Water, Coin Change.

### Q2: code repository + AI assistant
You get a small repo (several files, existing tests) and a task: fix a bug, add a feature, or implement a function so the tests pass. An AI assistant is available inside the IDE. **Using it well is part of the test**, not cheating.

**Routine:**
1. **Read the task and the README first.** Then skim the structure: entry point, the module you'll touch, the tests.
2. **Run the tests before changing anything** to see what fails and why.
3. Use the AI for **speed, not judgement**:
   - "Explain what `OrderService.process` does and where it's called."
   - "Which test covers discount calculation? Why is it failing?"
   - "Write a function that ... following the style in `utils.py`."
   - "Add a unit test for the empty-cart case."
4. **Read every line it generates.** Assistants make up method names, ignore edge cases, and change things you didn't ask for. Check that it uses the repo's existing helpers, types, and error handling.
5. Keep the diff **small and focused**: only change what the task needs. Don't let it refactor unrelated files.
6. Run the full test suite after each change. Add a test for the edge case you fixed.
7. If the assistant goes in circles twice, stop asking and debug it yourself (print/log, read the stack trace).

**Common traps:** off-by-one in boundaries, `None`/null handling, mutating input lists, integer vs float division, time zones, not updating every call site after a signature change.

---

## 2️⃣ Work Simulation (~45 min)

### What it looks like
You play an SDE on a fictional Amazon team for a "day". Messages arrive from your manager, teammates, a product manager, or customers (email, chat, short videos, dashboards). Each scenario asks you to either:
- choose the **best** (and sometimes **worst**) response,
- **rate each option** from very ineffective to very effective, or
- pick an option from data: a metrics table, error logs, a design comparison, test results.

There's no trick. It's checking whether your instincts match how Amazon wants SDEs to act. Answer as the **ideal Amazon engineer**, not as the most agreeable person in the room.

### The decision filter
When unsure, prefer the option that:
1. **Protects the customer** first (Customer Obsession). Customer impact beats internal convenience, deadlines, or looking good.
2. **Uses data** to decide, or gathers it quickly when missing (Dive Deep, Are Right A Lot).
3. **Acts now** on reversible decisions; doesn't wait for perfect info (Bias for Action). Slows down only for irreversible, high-risk ones.
4. **Takes ownership**: fixes it or drives it to the right owner, even if "not my code" (Ownership).
5. **Keeps quality high**: no shipping known bugs or skipping tests to hit a date (Insist on the Highest Standards).
6. **Communicates early and plainly**: tells the manager/stakeholders about risk, with options and a recommendation (Earn Trust).
7. **Disagrees respectfully with data, then commits** once a decision is made (Have Backbone; Disagree and Commit).
8. **Simplifies**: smallest solution that solves the real problem; reuse what exists (Invent and Simplify, Frugality).

**Usually wrong:** escalating before trying anything yourself; doing nothing and waiting; silently working around a problem; blaming another team; hiding a mistake; spending days on analysis for a reversible choice; over-engineering; promising a date you can't hit; saying yes to every request without checking priorities.

**Usually right but not best:** "ask my manager what to do" (fine, but the best answer usually comes **with a proposed plan**).

### Practice scenarios
Pick your answer before opening each one.

<details>
<summary><b>S1. Production issue.</b> You're on call. Checkout error rate jumped from 0.1% to 4% right after your teammate's deploy 20 minutes ago. Your teammate is offline. What do you do?<br>A) Wait for your teammate since it's their code · B) Roll back the deploy, then investigate and post an update · C) Start debugging the new code to find the exact bug before acting · D) Email the manager and wait for instructions</summary>

**Best: B.** Customers are failing to check out right now. Rollback is fast and reversible (Bias for Action, Customer Obsession). Then find the root cause, update stakeholders, and write a post-mortem (COE). **Worst: A.** C is tempting but leaves customers broken while you debug. D gives away ownership.

</details>

<details>
<summary><b>S2. Deadline vs quality.</b> Launch is in 2 days. You find an edge case where a small % of international orders get the wrong tax. A fix takes ~3 days. PM wants to launch on time.<br>A) Launch and fix later without telling anyone · B) Delay silently and keep working · C) Tell PM and manager the impact with data; propose options, e.g. launch with international orders behind a feature flag, then fix · D) Refuse to launch until everything is perfect</summary>

**Best: C.** Quantify the impact, give options, recommend one. Launching to most customers while protecting the affected ones balances Deliver Results with Highest Standards. **Worst: A** (hides a customer-facing bug; breaks trust). D is too rigid; B leaves stakeholders blind.

</details>

**S3 data.** Three caching options for a product page service (p99 latency SLA 200 ms):

| Option | p99 latency | Monthly cost | Effort |
|---|---|---|---|
| A: no cache, bigger DB | 240 ms | $9,000 | 1 week |
| B: Redis cache-aside | 60 ms | $2,500 | 2 weeks |
| C: custom in-memory cache + invalidation service | 40 ms | $1,800 | 8 weeks |

<details>
<summary><b>S3. Choosing a design from data.</b> Using the table above, which option do you recommend?</summary>

**Best: B.** Meets the SLA with margin, cheap, reasonable effort. **A** misses the SLA, so it's out regardless of effort. **C** is slightly better on paper but 4× the effort and more to maintain (Invent and Simplify, Frugality). The pattern: first eliminate options that fail a hard requirement, then pick the simplest one that meets it.

</details>

<details>
<summary><b>S4. Disagreeing with a senior engineer.</b> A senior engineer in a design review wants to use a new database. You have benchmark data showing it performs worse for your access pattern.<br>A) Stay quiet; they're senior · B) Share your benchmark in the review, explain the access pattern, and suggest testing both · C) Complain to your manager afterwards · D) Build your version anyway</summary>

**Best: B** (Have Backbone; Disagree and Commit, with data). If the team still chooses their option after hearing it, **commit fully**. **Worst: D** (undermines the team decision). A and C avoid the conflict instead of resolving it.

</details>

<details>
<summary><b>S5. Ambiguous request.</b> Your manager asks you to "make the report page faster". No other details.<br>A) Start rewriting the frontend right away · B) Measure where the time goes (backend queries, payload, rendering), check with the manager what "fast" means for users, then fix the biggest bottleneck first · C) Ask for a full spec before starting · D) Add more servers</summary>

**Best: B.** Clarify the goal briefly, measure, fix the biggest win (Dive Deep, Bias for Action). **A/D** guess without data. **C** waits too long on something you can figure out yourself.

</details>

<details>
<summary><b>S6. Code review.</b> A teammate's PR works, but has no tests and duplicates a helper that already exists. They want it merged today for a demo.<br>A) Approve; it works · B) Reject with "needs work" · C) Leave specific comments: point to the existing helper, ask for tests on the key paths, offer to pair so it's still ready today · D) Rewrite it yourself without telling them</summary>

**Best: C.** Keeps the bar (Highest Standards), is specific and kind, and helps hit the date (Deliver Results). **Worst: D** (no trust, no learning). A lowers the bar; B is unhelpful.

</details>

<details>
<summary><b>S7. Too many priorities.</b> You have a sprint task due Friday. A PM from another team asks you for "a quick feature" for their project. A customer-reported bug in your service also comes in.<br>Rank the order to handle them.</summary>

**Best order:** (1) Triage the customer bug: check severity and how many customers are hit; fix or mitigate if it's high impact. (2) Tell your manager about the conflict and agree on priority for the PM's request (don't silently say yes or no). (3) Continue the sprint task; flag early if Friday is at risk. Principle: customer impact first, make trade-offs visible, don't over-commit.

</details>

<details>
<summary><b>S8. You made a mistake.</b> You realize a script you ran yesterday deleted some test-environment data another team relies on.<br>A) Say nothing; it's only test data · B) Restore what you can, tell the affected team and your manager right away, explain what happened and how you'll prevent it · C) Quietly restore it and hope nobody noticed · D) Blame the unclear runbook</summary>

**Best: B** (Earn Trust, Ownership). Own it, fix it, prevent it (e.g. add a dry-run flag or confirmation). **Worst: A/C** (hiding), D (blame). Amazon rewards owning mistakes, not avoiding them.

</details>

<details>
<summary><b>S9. Reading logs.</b> An API's latency spiked. Logs show: DB query time flat at ~20 ms; calls to an external payments service went from 80 ms to 1,900 ms; CPU at 30%. Which action first?<br>A) Scale up the app servers · B) Add a DB index · C) Add a timeout + retry with backoff/circuit breaker on the payments call and contact that team · D) Rewrite the service</summary>

**Best: C.** The data points to the downstream dependency, not DB or CPU (Dive Deep). Protect your service from it and loop in the owning team. A and B fix things that aren't broken; D is overkill.

</details>

<details>
<summary><b>S10. Build vs reuse.</b> You need a rate limiter. An internal, well-supported library does it. A teammate wants to build a custom one "because it'd be fun and slightly faster".<br>A) Build custom · B) Use the library; build custom only if measurements show it can't meet requirements · C) Ask leadership to decide</summary>

**Best: B** (Frugality, Invent and Simplify). Reuse proven components; invest in custom only when data proves a need.

</details>

<details>
<summary><b>S11. Helping a new teammate.</b> A new hire keeps asking you questions, and it's slowing your own task.<br>A) Ignore them · B) Answer everything instantly · C) Set a short daily time to pair, point them to docs, and write down the common answers in the team wiki · D) Tell the manager they ask too much</summary>

**Best: C.** Helps them grow and scales the help (Hire and Develop the Best, Invent and Simplify), while protecting your delivery.

</details>

<details>
<summary><b>S12. Customer feedback vs roadmap.</b> Several customers report a confusing error message that causes support tickets. It's not on the roadmap, and fixing it is a small change.<br>A) Wait for next quarter's planning · B) Make the small fix now, with the manager's OK, and track ticket volume afterwards · C) Tell support to explain it better</summary>

**Best: B.** Small, reversible, clear customer benefit, and you measure the result (Customer Obsession, Bias for Action).

</details>

### Leadership Principles cheat sheet
| LP | What the "right" answer usually shows |
|---|---|
| Customer Obsession | Start from customer impact; fix customer pain before internal convenience |
| Ownership | "Not my team" is never the answer; long-term over short-term |
| Invent and Simplify | Simplest solution; reuse; remove complexity |
| Are Right, A Lot | Use data and judgement; seek out people who disagree |
| Learn and Be Curious | Ask questions, learn new areas |
| Hire and Develop the Best | Mentor, share knowledge, raise the bar |
| Insist on the Highest Standards | Tests, reviews, no known defects shipped silently |
| Think Big | Solve the class of problem when it's cheap to do so |
| Bias for Action | Act on reversible decisions; calculated risk |
| Frugality | Do more with less; cost-aware designs |
| Earn Trust | Be candid, own mistakes, communicate early |
| Dive Deep | Look at metrics/logs; know the details; find the root cause |
| Have Backbone; Disagree and Commit | Push back respectfully with data, then commit fully |
| Deliver Results | Hit the goal; when you can't, say so early and offer options |
| Strive to be Earth's Best Employer | Support teammates; inclusive, safe environment |
| Success and Scale Bring Broad Responsibility | Think about wider impact of decisions |

---

## 3️⃣ Work Style Survey (~6 min each)
Statements like *"I prefer to finish a task completely before starting another"* or a choice between two statements. There are no hard right answers, but it's scored for fit with the LPs and for **consistency** (the same trait gets asked several ways).

- Answer honestly and quickly. Overthinking leads to contradictions.
- Lean towards: taking ownership, acting with incomplete information, high standards, curiosity, using data, being comfortable with change and ambiguity, helping others, owning mistakes.
- Avoid extremes that read as rigid: "I never start without complete requirements", "I always do it exactly as told".
- If two statements both sound good, pick the one closer to **customer impact** or **ownership**.

---

## 📅 One-week plan
| Day | Coding (60–90 min) | Other (30–45 min) |
|---|---|---|
| 1 | Take the **demo test**, both questions | Read this page; LP table |
| 2 | Arrays/hashing, sliding window: 3 Amazon-tagged mediums, timed 30 min each | Work Simulation scenarios S1–S6, explain *why* out loud |
| 3 | Heaps, intervals, greedy: 3 mediums | Scenarios S7–S12 |
| 4 | Graphs (BFS/DFS, topo sort): 3 mediums | Practice a repo task: clone a small open-source Python project, run its tests, fix a bug or add a feature with an AI assistant, reviewing every line |
| 5 | Mock: 2 random Amazon mediums in 70 min | [Django questions](../../04_cs_fundamentals/06_django.md) (for later rounds) |
| 6 | Redo anything you missed this week | Rest. Check camera, ID, browser |
| 7 | **Take the OA** in the morning, fresh | — |

## After the OA
If you pass, the next rounds are usually a phone screen or straight to the loop: coding (DSA), **LLD/system design**, and **LP behavioral questions in every round**. Prepare 8–10 STAR stories in [05_behavioral](../../05_behavioral/README.md), each mapped to 2–3 LPs.
