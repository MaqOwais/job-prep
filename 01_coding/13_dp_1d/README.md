# 13. Dynamic Programming: 1-D

**Signals:** "number of ways", "minimum/maximum cost", "can you reach/form…", choices at each step that affect future choices, and a brute force with overlapping subproblems.

## The 5-step DP recipe (say this out loud in interviews)
1. **State:** `dp[i]` = the answer for the first i elements / for position i.
2. **Recurrence:** how `dp[i]` depends on smaller states.
3. **Base cases.**
4. **Order:** top-down (memoized recursion) or bottom-up (table).
5. **Answer location** + space optimization (often only the last 1–2 values are needed).

> Start with **top-down recursion + `@cache`**. It maps directly from brute force. Convert to bottom-up if asked.

## Templates
```python
from functools import cache

# House Robber: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
def rob(nums):
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

# Coin Change (unbounded, min count): dp[a] = min(dp[a - c] + 1)
def coin_change(coins, amount):
    dp = [0] + [float('inf')] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a: dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# Word Break (top-down)
def word_break(s, words):
    words = set(words)
    @cache
    def ok(i):
        if i == len(s): return True
        return any(s[i:j] in words and ok(j) for j in range(i + 1, len(s) + 1))
    return ok(0)

# LIS O(n log n): patience sorting
from bisect import bisect_left
def lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return len(tails)
```

## Common 1-D DP shapes
| Shape | Example | Recurrence |
|---|---|---|
| Fibonacci-like | Climbing Stairs | `dp[i] = dp[i-1] + dp[i-2]` |
| Take / skip | House Robber | `max(skip, take + dp[i-2])` |
| Unbounded knapsack | Coin Change | `min over coins` |
| Partition / segmentation | Word Break, Decode Ways | look back at valid cuts |
| LIS-style | LIS | `dp[i] = 1 + max(dp[j]) for j<i, a[j]<a[i]` |
| Kadane | Max Subarray | `cur = max(x, cur + x)` |
| Expand around center | Palindromic substrings | 2n−1 centers |

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Fibonacci |
| [ ] | [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` |
| [ ] | [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | Two variables |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [House Robber](https://leetcode.com/problems/house-robber/) | Take/skip |
| [ ] | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | Circular: max(rob(1..n), rob(0..n−1)) |
| [ ] | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Expand around center |
| [ ] | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | Expand around center, count |
| [ ] | [Decode Ways](https://leetcode.com/problems/decode-ways/) | 1-digit and 2-digit lookback |
| [ ] | [Coin Change](https://leetcode.com/problems/coin-change/) | Unbounded knapsack |
| [ ] | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Track both curMax and curMin |
| [ ] | [Word Break](https://leetcode.com/problems/word-break/) | Segmentation |
| [ ] | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | O(n²) DP → O(n log n) tails |
| [ ] | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 0/1 knapsack to sum/2 (set of reachable sums) |
| [ ] | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Kadane |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Word Break II](https://leetcode.com/problems/word-break-ii/) | Memoized DFS returning lists of sentences |
| [ ] | [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | Sort (w asc, h desc) → LIS on h |

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do you recognize a dynamic programming problem?</b></summary>

The problem asks for a **count, min/max, or yes/no** over choices, and a brute-force recursion **revisits the same subproblems** (overlapping subproblems) whose optimal answers combine into the overall answer (optimal substructure).

</details>

<details>
<summary><b>Q2. Top-down vs bottom-up DP?</b></summary>

**Top-down:** recursion + memoization (@cache). It maps directly from brute force and only computes the states it needs, but risks recursion limits. **Bottom-up:** fill a table iteratively in dependency order. No recursion overhead, and easier to optimize space. Start top-down in interviews, convert if asked.

</details>

<details>
<summary><b>Q3. Explain the House Robber recurrence and its O(1) space version.</b></summary>

dp[i] = max(dp[i−1], dp[i−2] + nums[i]): either skip house i or rob it plus the best up to i−2. Only the last two values are needed, so keep two variables (prev2, prev1).

</details>

<details>
<summary><b>Q4. How does Coin Change (minimum coins) work, and what's the complexity?</b></summary>

dp[a] = min over coins c ≤ a of dp[a − c] + 1, with dp[0] = 0 and infinity for unreachable amounts. **O(amount × coins)** time, O(amount) space. If dp[amount] is still infinity, return −1.

</details>

<details>
<summary><b>Q5. How do you get the longest increasing subsequence in O(n log n)?</b></summary>

Maintain **tails**, where tails[i] is the smallest possible tail of an increasing subsequence of length i + 1. For each x, bisect_left into tails to replace or append. len(tails) is the answer. Patience sorting.

</details>
