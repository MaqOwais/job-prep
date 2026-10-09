# 1. Arrays & Hashing

**Signals:** "find a pair/duplicate", "count frequency", "group by", "has this been seen before?", "subarray sum equals k".

## Core idea
Trade **space for time**: a `set`/`dict` makes "have I seen X?" an O(1) check, so an O(n²) nested loop becomes an O(n) single pass.
**Prefix sums** turn "sum of a subarray" into `prefix[j] - prefix[i]`, which is O(1) per query.

## Templates
```python
# 1) Seen-before (Two Sum)
def two_sum(nums, target):
    seen = {}                       # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i

# 2) Frequency / grouping
from collections import Counter, defaultdict
def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)   # or a 26-length count tuple → O(L) key
    return list(groups.values())

# 3) Prefix sum + hashmap (count subarrays with sum k, works with negatives)
def subarray_sum(nums, k):
    count, cur, seen = 0, 0, {0: 1}
    for x in nums:
        cur += x
        count += seen.get(cur - k, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return count

# 4) Bucket sort by frequency (Top K Frequent in O(n))
def top_k(nums, k):
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for x, c in freq.items():
        buckets[c].append(x)
    res = []
    for c in range(len(buckets) - 1, 0, -1):
        for x in buckets[c]:
            res.append(x)
            if len(res) == k:
                return res
```

## Pitfalls
- Lists aren't hashable. Use a `tuple` as the dict key.
- In Two Sum, check `target - x` **before** inserting `x`, so you don't pair an element with itself.
- Prefix-sum map: initialize it with `{0: 1}` to count subarrays that start at index 0.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | `len(set(nums)) != len(nums)` |
| [ ] | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | `Counter(s) == Counter(t)` |
| [ ] | [Two Sum](https://leetcode.com/problems/two-sum/) | Map from value to index; look up the complement |
| [ ] | [Majority Element](https://leetcode.com/problems/majority-element/) | Boyer-Moore voting gives O(1) space |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Key = sorted word or a 26-count tuple |
| [ ] | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Bucket sort by frequency → O(n) |
| [ ] | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Prefix products left to right, then suffix products right to left |
| [ ] | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | A set per row, column, and box `(r//3, c//3)` |
| [ ] | [Encode and Decode Strings](https://neetcode.io/problems/string-encode-and-decode) | Length prefix: `"4#word"` |
| [ ] | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Only start counting at x if `x-1` isn't in the set |
| [ ] | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Prefix sum + count map (template 3) |
| [ ] | [Contiguous Array](https://leetcode.com/problems/contiguous-array/) | Treat 0 as −1; first index of each prefix sum |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Use the array itself as a hash: place x at index x−1 |

## Go deeper
- [NeetCode: Arrays & Hashing](https://neetcode.io/practice)
- [Interactive Coding Challenges: arrays & strings, hash maps (by the primer's author)](https://github.com/donnemartin/interactive-coding-challenges)

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What's the time and space complexity of Two Sum with a hash map, and why check before inserting?</b></summary>

**O(n) time, O(n) space**: one pass, with an O(1) average lookup per element. Checking for target − x **before** inserting x prevents pairing an element with itself (e.g., target 6 with a single 3).

</details>

<details>
<summary><b>Q2. Why does 'Subarray Sum Equals K' need prefix sums + a hash map instead of a sliding window?</b></summary>

With **negative numbers**, expanding or shrinking the window doesn't move the sum monotonically, so sliding window logic breaks. Prefix sums turn "sum of nums[i..j] = k" into "prefix[j] − prefix[i−1] = k", and a count map of earlier prefix sums finds all matches in O(n).

</details>

<details>
<summary><b>Q3. How do you get Top K Frequent Elements in O(n)?</b></summary>

Count with a hash map, then **bucket sort by frequency**: an array where index = frequency holds lists of values. Walk from the highest frequency down until you've collected k values. A heap gives O(n log k) as the alternative.

</details>

<details>
<summary><b>Q4. Why is Longest Consecutive Sequence O(n) even with a nested while loop?</b></summary>

You only start counting from x when **x − 1 isn't in the set** (x is a sequence start). Each element is then visited at most once by an inner loop across all starts, so the total work is O(n).

</details>

<details>
<summary><b>Q5. When would a hash map's O(1) average become O(n), and does that matter in interviews?</b></summary>

When many keys collide (bad hash function or adversarial input), operations degrade to O(n). In interviews, state "**O(1) average**" and move on, unless asked about worst cases or security (hash flooding).

</details>
