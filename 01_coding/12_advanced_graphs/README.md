# 12. Advanced Graphs (Dijkstra, MST, Bellman-Ford)

**Signals:** **weighted** shortest path, "minimum cost to connect all", "at most k stops", "minimize the maximum edge on a path".

## Core ideas
| Algorithm | Use for | Complexity |
|---|---|---|
| **Dijkstra** | Shortest path, non-negative weights | O(E log V) |
| **Bellman-Ford** | Negative weights, or "at most k edges" | O(V·E), or O(k·E) for k rounds |
| **Prim / Kruskal** | Minimum spanning tree | O(E log V) / O(E log E) |
| **Floyd-Warshall** | All-pairs shortest paths, small V | O(V³) |
| Topological sort + DP | Shortest/longest path in a DAG | O(V + E) |

## Templates
```python
import heapq
from collections import defaultdict

# Dijkstra
def dijkstra(n, edges, src):
    g = defaultdict(list)
    for u, v, w in edges: g[u].append((v, w))
    dist = {}; h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if u in dist: continue               # already finalized
        dist[u] = d
        for v, w in g[u]:
            if v not in dist: heapq.heappush(h, (d + w, v))
    return dist

# Bellman-Ford limited to k edges (Cheapest Flights Within K Stops)
def k_stops(n, flights, src, dst, k):
    dist = [float('inf')] * n; dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]                        # copy! use last round's values
        for u, v, w in flights:
            if dist[u] + w < nxt[v]: nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == float('inf') else dist[dst]

# Prim's MST (Min Cost to Connect All Points)
def prim(points):
    n = len(points); seen = set(); h = [(0, 0)]; total = 0
    while len(seen) < n:
        cost, i = heapq.heappop(h)
        if i in seen: continue
        seen.add(i); total += cost
        for j in range(n):
            if j not in seen:
                d = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1])
                heapq.heappush(h, (d, j))
    return total
```

## Pitfalls
- Dijkstra doesn't work with negative edges.
- Bellman-Ford with k stops: **copy** the distance array each round.
- "Minimize the max edge on a path" → modified Dijkstra (use `max` instead of `+`), or binary search + BFS.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Find Center of Star Graph](https://leetcode.com/problems/find-center-of-star-graph/) | Warm-up: the node common to the first two edges |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Dijkstra; answer = max distance |
| [ ] | [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | Prim's |
| [ ] | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Bellman-Ford k+1 rounds |
| [ ] | [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Dijkstra with max instead of sum |
| [ ] | [Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/) | Dijkstra on −probability (max-heap) |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) | Dijkstra on max elevation |
| [ ] | [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | Hierholzer's (Eulerian path), lexical order |
| [ ] | [Alien Dictionary](https://neetcode.io/problems/foreign-dictionary) | Build edges from adjacent words → topo sort |
