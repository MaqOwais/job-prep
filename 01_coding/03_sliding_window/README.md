# 3. Sliding Window

**Signals:** "contiguous subarray/substring", "longest/shortest/max/min … such that …", "at most k", fixed window size k.

## Core idea
Keep a window `[l, r]`. **Expand** `r` every step. **Shrink** `l` while the window is invalid. Each element enters and leaves at most once, so the whole pass is O(n).

## Templates
```python
# Variable window — longest valid
def longest(s):
    count = {}; l = best = 0
    for r, c in enumerate(s):
        count[c] = count.get(c, 0) + 1          # 1. add right
        while count[c] > 1:                      # 2. shrink while INVALID
            count[s[l]] -= 1; l += 1
        best = max(best, r - l + 1)              # 3. record answer
    return best

# Variable window — shortest valid (record INSIDE the shrink loop)
def min_subarray_len(target, nums):
    l = total = 0; best = float('inf')
    for r, x in enumerate(nums):
        total += x
        while total >= target:                   # while VALID → try to shrink
            best = min(best, r - l + 1)
            total -= nums[l]; l += 1
    return 0 if best == float('inf') else best

# Fixed window of size k
def max_sum_k(nums, k):
    cur = sum(nums[:k]); best = cur
    for r in range(k, len(nums)):
        cur += nums[r] - nums[r - k]
        best = max(best, cur)
    return best
```

## Pitfalls
- **Longest** → record after shrinking. **Shortest** → record inside the shrink loop.
- Sliding windows don't work for sums with **negative numbers**. Use prefix sums + a hashmap instead.
- "Exactly k" = atMost(k) − atMost(k−1).

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Track the minimum price so far |
| [ ] | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Fixed window |
| [ ] | [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | A set holding the last k elements |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Shrink while there's a duplicate |
| [ ] | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Valid if `len − maxFreq ≤ k` |
| [ ] | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Fixed window, compare 26-letter counts |
| [ ] | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Shortest-valid template |
| [ ] | [Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Window with at most k zeros |
| [ ] | [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | At most 2 distinct values |
| [ ] | [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) | Add `r − l + 1` each step |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Need-count + a "formed" counter; shrink while valid |
| [ ] | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Monotonic decreasing **deque** of indices |
| [ ] | [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) | atMost(k) − atMost(k−1) |
