# 10. Backtracking

**Signals:** "all possible", "every combination/permutation/subset", "generate", N-Queens, Sudoku, word search in a grid. Constraints are usually small (n ≤ 20).

## Core idea
Explore a decision tree with three steps: **choose → explore → un-choose.** Prune branches that can't lead to a valid answer.

## Template
```python
def backtrack_template(nums):
    res, path = [], []
    def bt(start):
        res.append(path[:])                 # record (subsets: every node is an answer)
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:   # skip dups (needs sorted nums)
                continue
            path.append(nums[i])            # choose
            bt(i + 1)                       # explore (i → reuse allowed, i+1 → no reuse)
            path.pop()                      # un-choose
    nums.sort(); bt(0); return res

# Permutations: use a `used` array instead of `start`
def permute(nums):
    res, path, used = [], [], [False] * len(nums)
    def bt():
        if len(path) == len(nums): res.append(path[:]); return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True; path.append(nums[i])
            bt()
            path.pop(); used[i] = False
    bt(); return res

# Grid DFS backtracking (Word Search)
def exist(board, word):
    R, C = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word): return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]: return False
        tmp, board[r][c] = board[r][c], '#'          # mark visited
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)))
        board[r][c] = tmp                             # restore
        return found
    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
```

## Decision guide
| Problem type | `start` index? | Reuse elements? | Recurse with |
|---|---|---|---|
| Subsets | yes | no | `i + 1` |
| Combination Sum (reuse allowed) | yes | yes | `i` |
| Combination Sum II (no reuse, has duplicates) | yes + skip dups | no | `i + 1` |
| Permutations | no (`used[]`) | no | — |

## Pitfalls
- Append `path[:]` (a copy), not `path`.
- Always undo the choice (pop / unmark).
- Complexity: subsets O(n·2ⁿ), permutations O(n·n!).

## Problems
### 🟢 Easy
Start directly with Subsets (Medium). It's the "hello world" of backtracking.

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Subsets](https://leetcode.com/problems/subsets/) | Record at every node |
| [ ] | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Recurse with `i` (reuse) |
| [ ] | [Permutations](https://leetcode.com/problems/permutations/) | `used[]` |
| [ ] | [Subsets II](https://leetcode.com/problems/subsets-ii/) | Sort + skip dups |
| [ ] | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | Sort + skip dups + `i + 1` |
| [ ] | [Word Search](https://leetcode.com/problems/word-search/) | Grid DFS with in-place marking |
| [ ] | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Cut only if the prefix is a palindrome |
| [ ] | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | One level per digit |
| [ ] | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | open < n, close < open |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [N-Queens](https://leetcode.com/problems/n-queens/) | Sets for cols, `r+c`, `r−c` |
| [ ] | [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | Row/col/box sets; try 1–9 in each empty cell |
