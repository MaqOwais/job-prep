# 14. Dynamic Programming: 2-D

**Signals:** **two strings** (compare/transform), **grid paths**, knapsack with (item, capacity), "stock with cooldown/transactions" (state machine).

## Core idea
The state needs two indices: `dp[i][j]`. Draw the table, fill the first row and column (base cases), then fill the rest from neighbors.

## Templates
```python
# Two strings: Longest Common Subsequence
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Edit Distance: insert / delete / replace
def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

# Grid paths (space-optimized to one row)
def unique_paths(m, n):
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n): row[j] += row[j - 1]
    return row[-1]

# Top-down with state machine (stock with cooldown)
from functools import cache
def max_profit(prices):
    @cache
    def f(i, holding):
        if i >= len(prices): return 0
        skip = f(i + 1, holding)
        if holding: return max(skip, prices[i] + f(i + 2, False))   # sell + cooldown
        return max(skip, -prices[i] + f(i + 1, True))               # buy
    return f(0, False)
```

## Knapsack cheat sheet
| Type | Loop order (1-D array) |
|---|---|
| 0/1 (each item once) | items outer, capacity **descending** |
| Unbounded (reuse items) | items outer, capacity **ascending** |
| Count combinations (Coin Change II) | coins outer, amount inner |
| Count permutations | amount outer, coins inner |

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/) | Each cell = sum of the two cells above |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Unique Paths](https://leetcode.com/problems/unique-paths/) | `dp[i][j] = up + left` |
| [ ] | [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | min(up, left) + cell |
| [ ] | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Template |
| [ ] | [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | State machine (i, holding) |
| [ ] | [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Count combinations: coins in the outer loop |
| [ ] | [Target Sum](https://leetcode.com/problems/target-sum/) | Memo on (i, sum), or a subset-sum transform |
| [ ] | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | `dp[i][j]` = can s1[:i] and s2[:j] form s3[:i+j] |
| [ ] | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Template |
| [ ] | [Maximal Square](https://leetcode.com/problems/maximal-square/) | 1 + min(up, left, diagonal) |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | DFS + memo |
| [ ] | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | If equal: use + skip, else skip |
| [ ] | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Interval DP: choose the **last** balloon to burst in (l, r) |
| [ ] | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | `*` → zero occurrences, or one occurrence and stay |
