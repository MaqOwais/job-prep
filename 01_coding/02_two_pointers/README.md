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
