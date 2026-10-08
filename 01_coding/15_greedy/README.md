# 15. Greedy

**Signals:** "minimum number of …", "can you reach the end", scheduling, and a choice where a local optimum seems obviously safe.

## Core idea
Make the **locally best choice** at each step and never go back. It's fast (usually O(n) or O(n log n) with sorting), but you must be able to **justify** it. In interviews, give a one-line "exchange argument": *"Swapping any other choice for the greedy one never makes the answer worse."*
If you can't justify it, it's probably DP.

## Templates
```python
# Kadane (max subarray) — reset when the running sum hurts
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x); best = max(best, cur)
    return best

# Jump Game — track the farthest reachable index
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach: return False
        reach = max(reach, i + x)
    return True

# Jump Game II — BFS by "levels" of reach
def jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end: jumps += 1; end = far
    return jumps

# Gas Station — if total ≥ 0 a solution exists; restart after each failure
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost): return -1
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0: tank, start = 0, i + 1
    return start
```

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Assign Cookies](https://leetcode.com/problems/assign-cookies/) | Sort both; smallest cookie that satisfies each child |
| [ ] | [Lemonade Change](https://leetcode.com/problems/lemonade-change/) | Give change using the $10 bill first |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Kadane |
| [ ] | [Jump Game](https://leetcode.com/problems/jump-game/) | Farthest reach |
| [ ] | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Level-by-level reach |
| [ ] | [Gas Station](https://leetcode.com/problems/gas-station/) | Reset the start when the tank goes negative |
| [ ] | [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) | Counter + always start a group at the smallest card |
| [ ] | [Merge Triplets to Form Target Triplet](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) | Use only triplets that never exceed the target |
| [ ] | [Partition Labels](https://leetcode.com/problems/partition-labels/) | Last index of each character; cut when i == end |
| [ ] | [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) | Track the [min, max] range of open counts |
| [ ] | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | Sum every positive difference |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Candy](https://leetcode.com/problems/candy/) | Left pass, then right pass, take the max |
