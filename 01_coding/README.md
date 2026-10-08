# 🧩 Coding Rounds

There are 17 patterns. Each folder has: **when to use it (signals)**, **core idea**, **Python template**, **pitfalls**, and **problems ordered Easy → Medium → Hard with one-line hints**.

Don't read a hint until you've tried for 15 minutes. If you're still stuck after 30 minutes, read the solution, understand it, and add the problem to the [review queue](../00_start_here/progress_tracker.md#-review-queue-spaced-repetition).

## 📚 Pattern order
| # | Pattern | Core idea in one line |
|---|---|---|
| 0 | [Python toolkit](00_python_toolkit.md) | Interview-ready Python idioms + Big-O of built-ins |
| 1 | [Arrays & Hashing](01_arrays_hashing/) | Trade space for time with a set/dict, plus prefix sums |
| 2 | [Two Pointers](02_two_pointers/) | Sorted array or palindrome → move pointers inward |
| 3 | [Sliding Window](03_sliding_window/) | Contiguous subarray/substring → grow right, shrink left |
| 4 | [Stack](04_stack/) | Matching pairs, "next greater element" → (monotonic) stack |
| 5 | [Binary Search](05_binary_search/) | Sorted data, or searching over a monotonic answer space |
| 6 | [Linked List](06_linked_list/) | Dummy node, fast/slow pointers, in-place reversal |
| 7 | [Trees](07_trees/) | Recursion (DFS) or level by level (BFS) |
| 8 | [Tries](08_tries/) | Prefix lookups over many words |
| 9 | [Heap / Priority Queue](09_heap_priority_queue/) | Top-k, k-way merge, streaming median |
| 10 | [Backtracking](10_backtracking/) | Generate all combinations/permutations: choose → explore → un-choose |
| 11 | [Graphs](11_graphs/) | Grid/graph traversal, BFS shortest path, topological sort, union-find |
| 12 | [Advanced Graphs](12_advanced_graphs/) | Dijkstra, MST, Bellman-Ford |
| 13 | [1-D DP](13_dp_1d/) | Overlapping subproblems over one index |
| 14 | [2-D DP](14_dp_2d/) | Two strings, a grid, or (index, capacity) |
| 15 | [Greedy](15_greedy/) | The locally best choice is provably globally best |
| 16 | [Intervals](16_intervals/) | Sort by start, then merge or sweep |
| 17 | [Math & Bits](17_math_bits/) | XOR tricks, matrix manipulation, overflow |

---

## 🧭 The UMPIRE method (use it on every problem)
1. **U**nderstand: restate the problem, ask about constraints, write 2–3 test cases including edge cases.
2. **M**atch: which pattern? (See the table below.)
3. **P**lan: brute force first, then optimize. State the complexity *before* you code.
4. **I**mplement: clean code, good names, small helper functions.
5. **R**eview: dry-run your test cases line by line.
6. **E**valuate: time/space complexity, then tradeoffs and follow-ups.

## 🔍 Pattern recognition cheat sheet
| If the problem says… | Think… |
|---|---|
| "sorted array", "pair that sums to" | Two pointers or binary search |
| "contiguous subarray/substring", "longest/shortest with condition" | Sliding window |
| "subarray sum equals k" (with negatives) | Prefix sum + hashmap |
| "top k", "k-th largest", "k closest" | Heap (size k) or quickselect |
| "all combinations/permutations/subsets" | Backtracking |
| "minimum steps", "shortest path" in an unweighted graph/grid | BFS |
| "shortest path" with weights | Dijkstra |
| "dependencies", "ordering", "prerequisites" | Topological sort |
| "connected components", "are these connected?" | Union-find or DFS |
| "next greater/smaller element" | Monotonic stack |
| "number of ways", "min/max cost", "can you reach" | DP |
| "intervals", "meetings", "overlapping" | Sort + sweep |
| "prefix", "words in a dictionary" | Trie |
| "minimize the maximum" or "maximize the minimum" | Binary search on the answer |
| "in-place", "O(1) space" on a linked list | Fast/slow pointers, reversal |
| "every element appears twice except one" | XOR |
| Design a data structure with O(1) operations | Hashmap + doubly linked list / array |

## ⏱️ What complexity do the constraints allow?
(Python handles roughly 10⁷ simple operations per second.)

| n | Target complexity | Typical algorithm |
|---|---|---|
| n ≤ 10 | O(n!) | Permutations, backtracking |
| n ≤ 20 | O(2ⁿ) | Subsets, bitmask DP |
| n ≤ 500 | O(n³) | Triple loop, Floyd-Warshall |
| n ≤ 5,000 | O(n²) | Nested loops, 2-D DP |
| n ≤ 10⁶ | O(n log n) | Sorting, heap, binary search |
| n ≤ 10⁸ | O(n) | Single pass, two pointers, hashing |
| n > 10⁸ | O(log n) / O(1) | Binary search, math |

## 📏 Big-O of common data structures
| Structure | Access | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| Array / list | O(1) | O(n) | O(n) (O(1) amortized at the end) | O(n) | `list.pop(0)` is O(n). Use a deque. |
| Hash map / set | — | O(1) average | O(1) | O(1) | O(n) worst case |
| Deque | O(1) at ends | O(n) | O(1) at ends | O(1) at ends | BFS queue |
| Heap | O(1) min | O(n) | O(log n) | O(log n) | `heapq` is a min-heap |
| Balanced BST | O(log n) | O(log n) | O(log n) | O(log n) | `sortedcontainers` (not always available) |
| Trie | — | O(L) | O(L) | O(L) | L = word length |

Sorting: O(n log n). BFS/DFS on a graph: O(V + E).

---

## ⭐ Must-know 40 (redo these before every interview)
These cover every pattern. If you can solve all of them cold, you're ready for most interviews.

| # | Problem | Level | Pattern |
|---|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | 🟢 | Hashing |
| 2 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 🟡 | Hashing |
| 3 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | 🟡 | Hashing/heap |
| 4 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | 🟡 | Prefix |
| 5 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 🟡 | Hashing |
| 6 | [3Sum](https://leetcode.com/problems/3sum/) | 🟡 | Two pointers |
| 7 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | 🟡 | Two pointers |
| 8 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | 🔴 | Two pointers |
| 9 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 🟡 | Sliding window |
| 10 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | 🔴 | Sliding window |
| 11 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | 🟢 | Stack |
| 12 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | 🟡 | Monotonic stack |
| 13 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 🟡 | Binary search |
| 14 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 🟡 | Binary search on answer |
| 15 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | 🟢 | Linked list |
| 16 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | 🔴 | Heap |
| 17 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | 🟡 | Design |
| 18 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | 🟢 | Tree DFS |
| 19 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟡 | Tree BFS |
| 20 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | 🟡 | Tree DFS |
| 21 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 🟡 | Tree DFS |
| 22 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | 🔴 | Tree |
| 23 | [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | 🟡 | Trie |
| 24 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 🟡 | Heap |
| 25 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | 🔴 | Two heaps |
| 26 | [Subsets](https://leetcode.com/problems/subsets/) | 🟡 | Backtracking |
| 27 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | 🟡 | Backtracking |
| 28 | [Word Search](https://leetcode.com/problems/word-search/) | 🟡 | Backtracking |
| 29 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | 🟡 | Graph DFS/BFS |
| 30 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 🟡 | Multi-source BFS |
| 31 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | 🟡 | Topological sort |
| 32 | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | 🟡 | Dijkstra |
| 33 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | 🟢 | 1-D DP |
| 34 | [Coin Change](https://leetcode.com/problems/coin-change/) | 🟡 | 1-D DP |
| 35 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | 🟡 | 1-D DP |
| 36 | [Word Break](https://leetcode.com/problems/word-break/) | 🟡 | 1-D DP |
| 37 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | 🟡 | 2-D DP |
| 38 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | 🟡 | 2-D DP |
| 39 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | 🟡 | Intervals |
| 40 | [Jump Game](https://leetcode.com/problems/jump-game/) | 🟡 | Greedy |

---

## 🔗 Practice sources
- [NeetCode 150](https://neetcode.io/practice): the same pattern grouping as this folder, with a video for every problem
- [Blind 75](https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions): the original curated list
- [Grind 75](https://www.techinterviewhandbook.org/grind75): builds a schedule from your available hours
- [Interactive Coding Challenges](https://github.com/donnemartin/interactive-coding-challenges): from the System Design Primer's author, with Anki flashcards
- [Tech Interview Handbook: coding](https://www.techinterviewhandbook.org/coding-interview-prep/)
- Company-tagged problems: LeetCode → Problems → filter by company (Premium)
