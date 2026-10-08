# 9. Heap / Priority Queue

**Signals:** "k largest/smallest/closest", "merge k sorted", "median of a stream", scheduling by priority, "always pick the min/max next".

## Core idea
A heap gives O(1) access to the min and O(log n) push/pop.
- **Top-k largest → min-heap of size k.** Pop whenever it grows past k. O(n log k).
- **Two heaps** (max-heap for the lower half, min-heap for the upper half) → running median.
- Python `heapq` is a **min-heap**. Negate values to get a max-heap.

## Templates
```python
import heapq

# Top-k largest
def k_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k: heapq.heappop(h)
    return h            # h[0] is the k-th largest

# K-way merge
def merge_k(lists):
    h = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(h); out = []
    while h:
        v, i, j = heapq.heappop(h); out.append(v)
        if j + 1 < len(lists[i]):
            heapq.heappush(h, (lists[i][j + 1], i, j + 1))
    return out

# Running median
class MedianFinder:
    def __init__(self): self.lo, self.hi = [], []   # lo = max-heap (negated)
    def addNum(self, x):
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    def findMedian(self):
        if len(self.lo) > len(self.hi): return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

## Pitfalls
- Tuples are compared element by element. Add a tiebreaker index `(priority, i, obj)` so Python never tries to compare objects.
- Quickselect averages O(n) for k-th largest. Mention it as the follow-up.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Min-heap of size k |
| [ ] | [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | Max-heap via negation |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Max-heap of size k on −dist |
| [ ] | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Heap, or quickselect |
| [ ] | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Formula `(maxf−1)(n+1)+countMax`, or heap + cooldown queue |
| [ ] | [Design Twitter](https://leetcode.com/problems/design-twitter/) | Merge the followees' tweet lists with a heap (see [news feed SD](../../02_high_level_design/12_problems/medium/06_twitter_news_feed.md)) |
| [ ] | [Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) | Heap with key (−count, word) |
| [ ] | [Reorganize String](https://leetcode.com/problems/reorganize-string/) | Greedy: most frequent first, hold back the previous character |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Two heaps |
| [ ] | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | K-way merge |
| [ ] | [IPO](https://leetcode.com/problems/ipo/) | Sort by capital; max-heap of affordable profits |
