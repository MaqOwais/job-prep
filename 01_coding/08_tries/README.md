# 8. Tries (Prefix Trees)

**Signals:** "prefix", "starts with", autocomplete, a dictionary of words + searching a grid, wildcard search.

## Core idea
A tree where each edge is a character. Insert and search take O(L) for a word of length L, **no matter how many words are stored**. It's also used in the [typeahead system design](../../02_system_design/12_problems/medium/10_typeahead_autocomplete.md).

## Template
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.end = True

    def _find(self, s):
        node = self.root
        for c in s:
            if c not in node.children: return None
            node = node.children[c]
        return node

    def search(self, word):
        n = self._find(word); return bool(n and n.end)

    def starts_with(self, prefix):
        return self._find(prefix) is not None

# Wildcard '.' search → DFS over children
def search_wild(node, word, i=0):
    if i == len(word): return node.end
    if word[i] == '.':
        return any(search_wild(ch, word, i + 1) for ch in node.children.values())
    nxt = node.children.get(word[i])
    return bool(nxt) and search_wild(nxt, word, i + 1)
```

## Pitfalls
- Mark the end of a word (`end = True`). "app" is a prefix of "apple" but isn't a word unless it was inserted.
- Word Search II: **prune** found words from the trie, otherwise it times out.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Simple approach: compare characters. Trie approach: walk while there's a single child. |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | Template |
| [ ] | [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | DFS on `.` |
| [ ] | [Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) | Trie storing the top 3 at each node, or sort + bisect |
| [ ] | [Replace Words](https://leetcode.com/problems/replace-words/) | Shortest root prefix |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Word Search II](https://leetcode.com/problems/word-search-ii/) | Trie of words + grid DFS; remove found words |
