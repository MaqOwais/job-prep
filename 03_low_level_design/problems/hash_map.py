"""
🟢 Hash Map — separate chaining + dynamic resizing.

Primer: https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/hash_table/hash_map.ipynb
LeetCode: https://leetcode.com/problems/design-hashmap/

Talking points:
  - hash(key) % capacity picks a bucket; collisions handled by a list per bucket (chaining)
    vs open addressing (linear/quadratic probing) — chaining is simpler, probing is cache-friendlier
  - load factor = size / capacity; resize (double + rehash) when > 0.75 → amortized O(1)
  - worst case O(n) if every key collides (bad hash / adversarial input)
"""


class HashMap:
    def __init__(self, capacity: int = 8, max_load: float = 0.75):
        self.capacity = capacity
        self.max_load = max_load
        self.size = 0
        self.buckets: list[list[tuple]] = [[] for _ in range(capacity)]

    def _index(self, key) -> int:
        return hash(key) % self.capacity

    def put(self, key, value) -> None:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > self.max_load:
            self._resize(self.capacity * 2)

    def get(self, key, default=None):
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        return default

    def remove(self, key) -> bool:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self, new_capacity: int) -> None:
        old = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)

    def __len__(self):
        return self.size


if __name__ == "__main__":
    m = HashMap(capacity=2)
    for i in range(100):
        m.put(f"k{i}", i)
    assert len(m) == 100 and m.get("k42") == 42
    m.put("k42", -1)
    assert m.get("k42") == -1 and len(m) == 100
    assert m.remove("k0") and not m.remove("k0")
    assert m.get("missing", "x") == "x"
    assert m.capacity >= 128  # resized
    print("✅ Hash map tests passed")
