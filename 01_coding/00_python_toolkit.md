# 🐍 Python Toolkit for Coding Interviews

Everything you'll reach for during a coding round, with its cost.

## Imports to remember
```python
from collections import defaultdict, Counter, deque, OrderedDict
from heapq import heappush, heappop, heapify, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from functools import lru_cache, cache, reduce
from itertools import accumulate, combinations, permutations, product, pairwise
from math import inf, gcd, ceil, floor, sqrt, comb
from typing import List, Optional, Dict
```

## Lists
```python
a = [0] * n                      # 1-D
grid = [[0] * cols for _ in range(rows)]   # 2-D  ✅  (NOT [[0]*cols]*rows ❌ — shared rows!)
a.append(x); a.pop()             # O(1) — use list as a stack
a.pop(0)                         # O(n) ❌ — use deque instead
a.sort(key=lambda x: (x[1], -x[0]))  # sort by 2nd asc, then 1st desc
sorted(a, reverse=True)          # returns a new list
a[::-1]                          # reversed copy
a.index(x), a.count(x)           # O(n)
list(zip(a, b)), list(enumerate(a))
```

## Strings (immutable!)
```python
s.lower(), s.isalnum(), s.isdigit(), s.isalpha()
s.split(), " ".join(words)       # build strings with join, not += in a loop (O(n²))
ord('a'), chr(97)                # char ↔ int;  ord(c) - ord('a') → 0..25
s[::-1], s.startswith("ab"), s.find("x")   # find returns -1 if missing
```

## Dict / Set / Counter
```python
d = defaultdict(list); d[k].append(v)     # no KeyError
cnt = Counter(s); cnt.most_common(k)      # frequency map
d.get(k, 0)                               # default value
for k, v in d.items(): ...
seen = set(); seen.add(x); x in seen      # O(1) average
tuple(sorted(s))  # hashable key for anagrams;  lists are NOT hashable
```

## Deque (queue / BFS / sliding window)
```python
q = deque([start])
q.append(x); q.popleft()          # O(1) both ends
q.appendleft(x); q.pop()
```

## Heap (min-heap only!)
```python
h = []; heappush(h, (priority, item)); heappop(h)
heapify(arr)                      # O(n)
heappush(h, -x)                   # max-heap trick: negate
# keep top-k largest: min-heap of size k
for x in nums:
    heappush(h, x)
    if len(h) > k: heappop(h)
```

## Binary search helpers
```python
i = bisect_left(a, x)    # first index with a[i] >= x
j = bisect_right(a, x)   # first index with a[j] >  x
```

## Memoization
```python
@cache                         # Python 3.9+, same as lru_cache(maxsize=None)
def dp(i, j): ...
```

## Useful one-liners
```python
float('inf'), -float('inf')      # or math.inf
divmod(a, b)                     # (quotient, remainder)
a // b   # floor division (careful: -7 // 2 == -4); use int(a / b) to truncate toward 0
max(a, key=len), min(d, key=d.get)
any(...), all(...)
list(accumulate(nums))           # prefix sums
```

## Linked list / tree node definitions (LeetCode style)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
```

## Gotchas
- Python's default recursion limit is about 1000. For deep DFS, use `sys.setrecursionlimit(10**6)` or iterate instead.
- Default mutable arguments: `def f(a=[])` ❌
- `is` vs `==`: use `==` for values. Use `is` only for `None`.
- Integer overflow doesn't exist in Python, but mention it when discussing Java or C++.
- Copying: `a[:]` or `list(a)` is shallow. Use `copy.deepcopy` for nested structures.
