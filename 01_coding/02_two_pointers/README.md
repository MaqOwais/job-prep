# 2. Two Pointers

**Signals:** sorted array, "pair/triplet with sum", palindrome, "in-place", removing duplicates, merging two sorted arrays.

## Core idea
Two indices move toward each other (**opposite ends**) or in the same direction (**fast/slow**). Each step throws out impossible candidates, so you get O(n) instead of O(n²).

## Templates
```python
# Opposite ends (sorted input)
def two_sum_sorted(a, target):
    l, r = 0, len(a) - 1
    while l < r:
        s = a[l] + a[r]
        if s == target: return [l, r]
        if s < target: l += 1      # need bigger
        else: r -= 1               # need smaller

# Same direction: write pointer (remove/move in place)
def move_zeroes(a):
    w = 0
    for r in range(len(a)):
        if a[r] != 0:
            a[w], a[r] = a[r], a[w]
            w += 1

# 3Sum = sort + fix one + two-pointer the rest (skip duplicates!)
def three_sum(nums):
    nums.sort(); res = []
    for i, x in enumerate(nums):
        if i and x == nums[i - 1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = x + nums[l] + nums[r]
            if s < 0: l += 1
            elif s > 0: r -= 1
            else:
                res.append([x, nums[l], nums[r]]); l += 1
                while l < r and nums[l] == nums[l - 1]: l += 1
    return res
```

## Pitfalls
- Skip duplicates in 3Sum/4Sum, both for the fixed element and after a match.
- `while l < r` vs `l <= r`: decide whether the pointers can point at the same element.
- Two pointers usually requires **sorted** data. Sorting costs O(n log n). Mention it.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Skip non-alphanumeric characters, compare lowercase |
| [ ] | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Fill from the **back** |
| [ ] | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Write pointer |
| [ ] | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Write pointer, compare with the previous kept value |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Opposite ends |
| [ ] | [3Sum](https://leetcode.com/problems/3sum/) | Sort + fix one + two pointers |
| [ ] | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Move the **shorter** wall inward |
| [ ] | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Dutch national flag: 3 pointers |
| [ ] | [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/) | Sort; pair the heaviest with the lightest |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Water = min(maxLeft, maxRight) − h. Move the side with the smaller max. |

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. When does the two-pointer technique apply?</b></summary>

When the input is **sorted** (or you can sort it), and a pointer move lets you **discard candidates**: pair or triplet sums, palindromes, merging sorted arrays, partitioning in place, removing duplicates. The signal is a monotonic relationship between the pointer moves and the result.

</details>

<details>
<summary><b>Q2. Why is 3Sum O(n²), and how do you avoid duplicate triplets?</b></summary>

Sort (O(n log n)), then for each i run a two-pointer scan over the rest (O(n)) → O(n²) total. Avoid duplicates by **skipping equal values** for i and, after finding a match, advancing l past equal neighbors.

</details>

<details>
<summary><b>Q3. In Container With Most Water, why move the shorter wall?</b></summary>

The area is limited by the **shorter** wall. Moving the taller wall inward can only reduce the width without raising the limiting height, so it can never improve the area. Moving the shorter wall is the only move that might find a taller limit.

</details>

<details>
<summary><b>Q4. Explain the two-pointer solution to Trapping Rain Water.</b></summary>

Water at i = min(maxLeft, maxRight) − height[i]. Keep l and r with leftMax and rightMax. **Move the side with the smaller max**: its water is determined by its own max, since the other side is known to be at least as tall. O(n) time, O(1) space.

</details>

<details>
<summary><b>Q5. What's the difference between opposite-end pointers and fast/slow pointers?</b></summary>

**Opposite ends** converge toward the middle (sorted pair sums, palindromes). **Same direction** (read/write or fast/slow) moves both forward at different speeds (remove duplicates in place, move zeroes, cycle detection in linked lists).

</details>
