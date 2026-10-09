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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do you justify that a greedy choice is correct?</b></summary>

With an **exchange argument**: take any optimal solution and show you can swap in the greedy choice without making it worse. Or show the greedy choice "stays ahead" at every step. If you can't argue it, it's probably DP.

</details>

<details>
<summary><b>Q2. How does Jump Game work greedily?</b></summary>

Track the **farthest index reachable** so far. Scan left to right. If the current index exceeds the reach, return false. Otherwise update reach = max(reach, i + nums[i]). O(n).

</details>

<details>
<summary><b>Q3. Explain Kadane's algorithm.</b></summary>

At each element, either **extend** the previous subarray or **start fresh**: cur = max(x, cur + x), and best = max(best, cur). A negative running sum never helps a future subarray, so you drop it. O(n), O(1) space.

</details>

<details>
<summary><b>Q4. Why does Gas Station's 'reset the start' trick work?</b></summary>

If the tank goes negative going from start to i, **no station between start and i** can be a valid start either (each would arrive at i with even less gas). So jump the start to i + 1. If the total gas ≥ total cost, the last start is valid.

</details>

<details>
<summary><b>Q5. Give a problem where greedy fails but DP works.</b></summary>

**Coin change with arbitrary denominations**: coins {1, 3, 4} for amount 6. Greedy takes 4 + 1 + 1 = 3 coins, but the optimum is 3 + 3 = 2 coins. Greedy is only safe for canonical coin systems like US coins.

</details>
