# 11. Graphs (DFS, BFS, Topological Sort, Union-Find)

**Signals:** grid of cells ("islands", "regions"), "connected", "shortest number of steps", "prerequisites/dependencies", "clone graph".

## Core ideas
| Need | Use |
|---|---|
| Visit everything / count components | DFS or BFS + `visited` |
| **Shortest path in an unweighted graph** | **BFS** |
| Spread from many sources at once (rotting oranges) | **Multi-source BFS** |
| Ordering with dependencies / cycle detection in a directed graph | **Topological sort (Kahn's BFS)** |
| Dynamic connectivity / cycle detection in an undirected graph | **Union-Find (DSU)** |

Build an adjacency list: `graph = defaultdict(list); for a, b in edges: graph[a].append(b)`.

## Templates
```python
from collections import deque, defaultdict
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Grid DFS (count islands)
def num_islands(grid):
    R, C = len(grid), len(grid[0]); count = 0
    def dfs(r, c):
        if not (0 <= r < R and 0 <= c < C) or grid[r][c] != '1': return
        grid[r][c] = '0'                     # mark visited
        for dr, dc in DIRS: dfs(r + dr, c + dc)
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1': dfs(r, c); count += 1
    return count

# BFS shortest path (also multi-source: put all sources in the queue first)
def bfs(start, neighbors):
    q, dist = deque([start]), {start: 0}
    while q:
        u = q.popleft()
        for v in neighbors(u):
            if v not in dist:
                dist[v] = dist[u] + 1; q.append(v)
    return dist

# Topological sort — Kahn's algorithm
def topo_sort(n, edges):                  # edge (a, b): a before b
    g, indeg = defaultdict(list), [0] * n
    for a, b in edges: g[a].append(b); indeg[b] += 1
    q = deque(i for i in range(n) if indeg[i] == 0); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return order if len(order) == n else []   # [] → cycle

# Union-Find with path compression + union by size
class DSU:
    def __init__(self, n): self.p, self.sz = list(range(n)), [1] * n
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: return False                # already connected → cycle
        if self.sz[a] < self.sz[b]: a, b = b, a
        self.p[b] = a; self.sz[a] += self.sz[b]; return True
```

## Pitfalls
- Mark nodes visited **when you enqueue them**, not when you dequeue them. Otherwise nodes get added twice.
- Directed vs undirected: for undirected graphs, add both edge directions.
- Recursive DFS on a 10⁶-cell grid can overflow the stack. Use BFS or an explicit stack.
- Complexity: O(V + E). For a grid, that's O(R·C).

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Flood Fill](https://leetcode.com/problems/flood-fill/) | Grid DFS |
| [ ] | [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) | BFS or DSU |
| [ ] | [Find the Town Judge](https://leetcode.com/problems/find-the-town-judge/) | In-degree − out-degree = n − 1 |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Grid DFS, count starts |
| [ ] | [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | DFS returns the area |
| [ ] | [Clone Graph](https://leetcode.com/problems/clone-graph/) | Map old → new + DFS |
| [ ] | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS by minute |
| [ ] | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Reverse: DFS uphill from each ocean, then intersect |
| [ ] | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Mark border-connected O's first |
| [ ] | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Kahn's: can all nodes be processed? |
| [ ] | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Return the topo order |
| [ ] | [Number of Connected Components](https://neetcode.io/problems/count-connected-components) | DSU |
| [ ] | [Graph Valid Tree](https://neetcode.io/problems/valid-tree) | n−1 edges + no cycle (DSU) |
| [ ] | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | First edge where union returns False |
| [ ] | [01 Matrix](https://leetcode.com/problems/01-matrix/) | Multi-source BFS from all zeros |
| [ ] | [Walls and Gates](https://neetcode.io/problems/islands-and-treasure) | Multi-source BFS from the gates |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Word Ladder](https://leetcode.com/problems/word-ladder/) | BFS; neighbors via wildcard patterns `h*t` |
| [ ] | [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | DFS + memo (a DAG) |

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. BFS vs DFS: which finds shortest paths, and why?</b></summary>

**BFS**, in **unweighted** graphs: it explores in order of distance (level by level), so the first time it reaches a node is via a shortest path. DFS gives no such guarantee. For weighted graphs, use Dijkstra.

</details>

<details>
<summary><b>Q2. Why mark nodes visited when enqueuing rather than when dequeuing in BFS?</b></summary>

Otherwise the same node can be **enqueued many times** by different neighbors before it's processed, wasting time and memory (and it can break distance counting).

</details>

<details>
<summary><b>Q3. How does Kahn's algorithm detect a cycle?</b></summary>

Repeatedly remove nodes with in-degree 0 and decrement their neighbors. If the number of processed nodes is **less than n** at the end, some nodes never reached in-degree 0, which means there's a **cycle**.

</details>

<details>
<summary><b>Q4. What do path compression and union by size do in union-find?</b></summary>

**Path compression** makes nodes on a find path point closer to (or directly at) the root. **Union by size/rank** attaches the smaller tree under the larger. Together, operations are nearly O(1) amortized (inverse Ackermann).

</details>

<details>
<summary><b>Q5. What is multi-source BFS? Give an example.</b></summary>

Start the BFS with **all sources in the queue at distance 0**, so the distances spread outward from every source at once. Rotting Oranges (all rotten oranges spread together) and 01 Matrix (distance to the nearest 0) are classic examples.

</details>
