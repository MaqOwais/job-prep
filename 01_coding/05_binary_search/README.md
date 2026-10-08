# 5. Binary Search

**Signals:** sorted input, "find in O(log n)", rotated array, **"minimum X such that…" / "maximum X such that…"** (binary search on the answer).

## Core idea
Halve the search space every step. It works whenever there's a **monotonic yes/no condition**: `F F F F T T T`. Find the first `T`.

## Templates
```python
# Classic: exact match
def search(a, target):
    l, r = 0, len(a) - 1
    while l <= r:
        m = (l + r) // 2
        if a[m] == target: return m
        if a[m] < target: l = m + 1
        else: r = m - 1
    return -1

# ⭐ Universal: first index where condition(m) is True (lower bound)
def first_true(lo, hi, condition):
    while lo < hi:
        m = (lo + hi) // 2
        if condition(m): hi = m      # m might be the answer, keep it
        else: lo = m + 1
    return lo

# Binary search on the ANSWER (Koko Eating Bananas)
from math import ceil
def min_eating_speed(piles, h):
    return first_true(1, max(piles),
                      lambda k: sum(ceil(p / k) for p in piles) <= h)

# Rotated sorted array: one half is always sorted
def search_rotated(a, t):
    l, r = 0, len(a) - 1
    while l <= r:
        m = (l + r) // 2
        if a[m] == t: return m
        if a[l] <= a[m]:                      # left half sorted
            if a[l] <= t < a[m]: r = m - 1
            else: l = m + 1
        else:                                 # right half sorted
            if a[m] < t <= a[r]: l = m + 1
            else: r = m - 1
    return -1
```

## Pitfalls
- Infinite loops: with `lo < hi` and `hi = m`, compute `m` with floor division. If you write `lo = m`, use `m = (lo + hi + 1) // 2`.
- Off-by-one errors: pick **one** template and always use it.
- In Python, `bisect_left`/`bisect_right` do this for you on sorted lists.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Binary Search](https://leetcode.com/problems/binary-search/) | Classic template |
| [ ] | [First Bad Version](https://leetcode.com/problems/first-bad-version/) | `first_true` |
| [ ] | [Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Lower bound |
| [ ] | [Sqrt(x)](https://leetcode.com/problems/sqrtx/) | Last m with m·m ≤ x |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Treat it as a 1-D array: `r, c = divmod(m, cols)` |
| [ ] | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Binary search the speed |
| [ ] | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Compare `a[m]` with `a[r]` |
| [ ] | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | One half is sorted |
| [ ] | [Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | `bisect_left` and `bisect_right − 1` |
| [ ] | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Per-key list of (timestamp, value); bisect |
| [ ] | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Binary search capacity in [max, sum] |
| [ ] | [Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Move toward the bigger neighbor |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Binary search the partition in the smaller array |
| [ ] | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Binary search the max sum; greedy count of pieces |
