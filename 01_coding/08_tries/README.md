# 8. Tries (Prefix Trees)

**Signals:** "prefix", "starts with", autocomplete, a dictionary of words + searching a grid, wildcard search.

## Core idea
A tree where each edge is a character. Insert and search take O(L) for a word of length L, **no matter how many words are stored**. It's also used in the [typeahead system design](../../02_high_level_design/12_problems/medium/10_typeahead_autocomplete.md).

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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. When is a trie better than a hash set of words?</b></summary>

When you need **prefix** operations: starts-with checks, autocomplete, listing all words with a prefix, or pruning a search (Word Search II) as soon as a prefix doesn't exist. A hash set only answers whole-word membership.

</details>

<details>
<summary><b>Q2. What are the complexities of trie insert and search?</b></summary>

**O(L)** time for a word of length L, independent of the number of words stored. Space is O(total characters) in the worst case. Using dicts for children saves space versus fixed 26-element arrays.

</details>

<details>
<summary><b>Q3. Why does each node need an end-of-word flag?</b></summary>

To distinguish a stored word from a mere prefix: after inserting "apple", the path for "app" exists, but "app" wasn't inserted unless that node is marked as an end.

</details>

<details>
<summary><b>Q4. How do you implement wildcard search like 'b.d'?</b></summary>

DFS: for a normal character, follow that child. For '.', **try every child** recursively. Return true if any branch reaches the end of the pattern at an end-of-word node. The worst case branches widely, but the trie prunes dead prefixes.

</details>

<details>
<summary><b>Q5. Why does Word Search II use a trie instead of searching each word separately?</b></summary>

Searching each word separately repeats the grid DFS once per word. With a trie of all the words, **one DFS per cell** explores every word at once and stops as soon as the current path isn't a prefix of any word. Removing found words keeps it fast.

</details>
