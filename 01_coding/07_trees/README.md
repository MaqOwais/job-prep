# 7. Trees (Binary Tree & BST)

**Signals:** "binary tree", "BST", depth, path, ancestor, level by level, serialize.

## Core ideas
- **DFS (recursion):** ask "what does each child need to return to its parent?" Most tree problems come down to designing that return value.
- **BFS (queue):** level-order traversal, right-side view, minimum depth.
- **BST property:** left < node < right. An **in-order traversal is sorted.**
- Traversals: pre-order (node, L, R), in-order (L, node, R), post-order (L, R, node).

## Templates
```python
# DFS returning a value (height) + updating a global answer (diameter)
def diameter(root):
    best = 0
    def h(node):
        nonlocal best
        if not node: return 0
        l, r = h(node.left), h(node.right)
        best = max(best, l + r)          # answer through this node
        return 1 + max(l, r)             # what the parent needs
    h(root); return best

# BFS level order
from collections import deque
def level_order(root):
    if not root: return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # process exactly one level
            n = q.popleft(); level.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        res.append(level)
    return res

# Validate BST with bounds
def is_bst(node, lo=float('-inf'), hi=float('inf')):
    if not node: return True
    if not lo < node.val < hi: return False
    return is_bst(node.left, lo, node.val) and is_bst(node.right, node.val, hi)

# Iterative in-order (k-th smallest in BST)
def kth_smallest(root, k):
    st, cur = [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); k -= 1
        if k == 0: return cur.val
        cur = cur.right
```

## Pitfalls
- BST validation: checking only against the direct children is **wrong**. Pass bounds down.
- Base case `if not node`. Handle an empty tree.
- Recursion depth on skewed trees can reach about 10⁵. Mention the iterative alternative.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Swap children recursively |
| [ ] | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | `1 + max(l, r)` |
| [ ] | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Height + global best |
| [ ] | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Return −1 if unbalanced |
| [ ] | [Same Tree](https://leetcode.com/problems/same-tree/) | Compare recursively |
| [ ] | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | sameTree at every node |
| [ ] | [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | mirror(a.left, b.right) |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Lowest Common Ancestor of a BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Split point where p and q go different ways |
| [ ] | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS by level |
| [ ] | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | Last node of each level |
| [ ] | [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | Pass the max seen so far down |
| [ ] | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Bounds |
| [ ] | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | In-order traversal |
| [ ] | [Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Preorder[0] = root; split the inorder list at it (index map) |
| [ ] | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | If both sides return non-null, this node is the LCA |
| [ ] | [Path Sum II](https://leetcode.com/problems/path-sum-ii/) | DFS + backtracking path |
| [ ] | [Binary Tree Zigzag Level Order](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | BFS, reverse every other level |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Return max single-branch gain (≥ 0); global = node + l + r |
| [ ] | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Pre-order with "N" for null |
