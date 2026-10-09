# 16. Intervals

**Signals:** `[start, end]` pairs, meetings, bookings, overlapping ranges, "minimum rooms", "remove the fewest to make non-overlapping".

## Core idea
**Sort**, then sweep:
- Merging / inserting → sort by **start**
- Max non-overlapping / min removals / arrows → sort by **end** (greedy)
- Max simultaneous overlaps (meeting rooms) → **min-heap of end times**, or a sweep line of +1/−1 events

Two intervals `[a, b]` and `[c, d]` overlap iff `a <= d and c <= b` (strictness depends on the problem).

## Templates
```python
import heapq

def merge_intervals(intervals):
    intervals.sort()
    res = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= res[-1][1]: res[-1][1] = max(res[-1][1], e)
        else: res.append([s, e])
    return res

def erase_overlap(intervals):             # min removals
    intervals.sort(key=lambda x: x[1])
    end, keep = float('-inf'), 0
    for s, e in intervals:
        if s >= end: keep += 1; end = e
    return len(intervals) - keep

def min_meeting_rooms(intervals):
    intervals.sort(); h = []
    for s, e in intervals:
        if h and h[0] <= s: heapq.heappop(h)  # reuse a freed room
        heapq.heappush(h, e)
    return len(h)
```

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Meeting Rooms](https://neetcode.io/problems/meeting-schedule) | Sort; any overlap → False |
| [ ] | [Summary Ranges](https://leetcode.com/problems/summary-ranges/) | Extend while consecutive |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Sort by start |
| [ ] | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Add the ones before, merge the overlapping ones, add the ones after |
| [ ] | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Sort by end, greedy |
| [ ] | [Meeting Rooms II](https://neetcode.io/problems/meeting-schedule-ii) | Min-heap of end times |
| [ ] | [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | Sort by end |
| [ ] | [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | Two pointers; advance the one that ends first |
| [ ] | [Car Pooling](https://leetcode.com/problems/car-pooling/) | Sweep line with a +/− diff array |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/) | Sort queries + heap of (size, end) |
| [ ] | [Employee Free Time](https://leetcode.com/problems/employee-free-time/) (🔒 Premium) | Merge all intervals, then find the gaps |

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why sort by start time for merging but by end time for maximum non-overlapping intervals?</b></summary>

**Merging:** sorted by start, overlapping intervals are adjacent, so you extend the current one. **Maximum non-overlapping / minimum removals:** greedily keep the interval that **ends earliest**, which leaves the most room for the rest (an exchange argument).

</details>

<details>
<summary><b>Q2. How do you compute the minimum number of meeting rooms?</b></summary>

Sort by start. Keep a **min-heap of end times** for rooms in use. For each meeting, free a room if the earliest end ≤ this start, then push this meeting's end. The heap's maximum size (its final size) is the answer. Alternatively, sweep a +1/−1 event line.

</details>

<details>
<summary><b>Q3. What's the condition for two intervals to overlap?</b></summary>

[a, b] and [c, d] overlap iff **a ≤ d and c ≤ b** (use < instead of ≤ if touching endpoints don't count). Equivalently: max(starts) ≤ min(ends).

</details>

<details>
<summary><b>Q4. How do you insert a new interval into a sorted, non-overlapping list?</b></summary>

Three phases: add every interval that **ends before** the new one starts, **merge** every interval overlapping the new one (expand its start and end), then add the rest. O(n).

</details>

<details>
<summary><b>Q5. How would you find the free time common to several people's calendars?</b></summary>

Flatten all busy intervals, **sort and merge** them, then the **gaps** between consecutive merged intervals are the common free time. Or k-way merge the per-person sorted lists with a heap.

</details>
