# 6. Linked List

**Signals:** "linked list" in the prompt, in-place reorder, cycle, "k-th from the end", merging sorted lists.

## Core ideas
1. **Dummy node:** avoids special cases when the head can change.
2. **Fast/slow pointers:** find the middle, detect a cycle, find the k-th node from the end.
3. **In-place reversal:** `prev, cur` pointer dance.
4. Draw the pointers on paper. Most bugs here are lost references.

## Templates
```python
# Reverse
def reverse(head):
    prev, cur = None, head
    while cur:
        cur.next, prev, cur = prev, cur, cur.next
    return prev

# Middle (slow ends at the middle; 2nd middle for even length)
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow

# Cycle detection (Floyd)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast: return True
    return False

# Merge two sorted lists with a dummy
def merge(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val: tail.next, a = a, a.next
        else: tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

## Pitfalls
- Save `cur.next` **before** you overwrite it.
- Null checks: `while fast and fast.next`.
- Return `dummy.next`, not `dummy`.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Iterative + recursive versions |
| [ ] | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Dummy node |
| [ ] | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Floyd |
| [ ] | [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Fast/slow |
| [ ] | [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | Middle + reverse the 2nd half + compare |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Reorder List](https://leetcode.com/problems/reorder-list/) | Middle → reverse 2nd half → interleave |
| [ ] | [Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Fast pointer starts n steps ahead; dummy node |
| [ ] | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Map old node → new node (2 passes) |
| [ ] | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Carry; `while a or b or carry` |
| [ ] | [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | After meeting, reset one pointer to head; step both by 1 |
| [ ] | [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | Array as linked list + Floyd |
| [ ] | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Hashmap + doubly linked list ([LLD version](../../03_low_level_design/problems/lru_cache.py)) |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Min-heap of `(val, i, node)` |
| [ ] | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Check that k nodes exist, reverse them, reconnect |
