# Interview Day Checklist

## Night before
- [ ] Light review only: the [must-know 40](../01_coding/README.md#-must-know-40-redo-these-before-every-interview) titles plus your story bank headlines
- [ ] Test camera, mic, internet, and the coding/whiteboard tool (CoderPad, HackerRank, Excalidraw, etc.)
- [ ] Sleep 7+ hours

## 30 minutes before
- [ ] Water, pen, paper
- [ ] Close notifications and other apps
- [ ] Have your story bank open on a second screen (keywords only)
- [ ] Re-read the "Golden rules" below

---

## 🧩 Coding round: the 45-minute script
| Minutes | Do this | Say something like |
|---|---|---|
| 0–5 | **Clarify** inputs, outputs, constraints, edge cases | "Can the array be empty? Negative numbers? How big can n get?" |
| 5–8 | **Examples:** walk through 1 normal and 1 edge case | "So for `[2,7,11]` with target 9, I'd return `[0,1]`." |
| 8–12 | **Brute force** + its complexity | "The naive way is O(n²). I'll check every pair." |
| 12–15 | **Optimize** by naming the pattern | "Since we need fast lookups, a hashmap gets this to O(n)." |
| 15–35 | **Code** cleanly, talking as you go | "I'll store each value's index as I scan…" |
| 35–40 | **Test** by dry-running your examples + edge cases | "Let me trace through `[3,3]`…" |
| 40–45 | **Complexity** + follow-ups | "O(n) time, O(n) space. If memory were tight, I could sort first…" |

**If you get stuck:** say what you're thinking, try a smaller example, think about what data structure would make the slow step fast, or ask "Would a hint be OK?"

## 🏗️ System design round: the 45–60-minute script
| Minutes | Step |
|---|---|
| 0–5 | Functional + non-functional requirements. **Ask; don't assume.** |
| 5–10 | Back-of-envelope estimates: QPS, storage, bandwidth |
| 10–15 | API design + data model |
| 15–25 | High-level diagram: client → LB → services → DB/cache/queue |
| 25–45 | Deep dive on 2–3 components the interviewer cares about |
| 45–55 | Bottlenecks, failure handling, scaling, tradeoffs |
| 55–60 | Summarize + ask your questions |

## 🗣️ Behavioral round
- STAR in 2–3 minutes. Say "I", not "we". Give numbers. End with what you learned.
- It's fine to pause: "Let me think of the best example."

---

## Golden rules
1. **Think out loud.** Silence hurts your score more than a wrong idea does.
2. **Clarify before solving.** Every round.
3. **State tradeoffs.** There's no single right answer in design.
4. **Don't bluff.** Say "I'm not sure, but here's how I'd reason about it."
5. **Ask 1–2 real questions** at the end of every round.

## After
- [ ] Write down every question you were asked, while it's fresh
- [ ] Send a thank-you note to the recruiter
- [ ] Add any problem you struggled with to the review list in the [tracker](progress_tracker.md)
