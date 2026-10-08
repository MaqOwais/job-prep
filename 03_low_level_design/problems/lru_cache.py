"""
🟢 LRU Cache — O(1) get/put using a hashmap + doubly linked list.

Primer: https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/lru_cache/lru_cache.ipynb
LeetCode: https://leetcode.com/problems/lru-cache/

Design:
  - dict: key -> Node                      (O(1) lookup)
  - doubly linked list: most recent at the head, least recent at the tail (O(1) move/remove)
  - sentinel head/tail nodes remove the edge cases
Follow-ups: thread safety (add a lock), TTL per entry, LFU variant, distributed version
(see 02_system_design/12_problems/easy/03_key_value_cache.md).
"""


class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()  # sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    # --- linked list helpers ---
    def _remove(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    # --- public API ---
    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_front(node)  # mark as most recently used
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.capacity:
            lru = self.tail.prev  # least recently used
            self._remove(lru)
            del self.map[lru.key]


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1  # order: 1, 2
    c.put(3, 3)  # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)  # evicts 1
    assert c.get(1) == -1
    assert c.get(3) == 3 and c.get(4) == 4
    print("✅ LRU cache tests passed")
