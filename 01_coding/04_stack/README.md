# 4. Stack (incl. Monotonic Stack)

**Signals:** matching brackets, "undo", nested structures (decode strings, calculators), **"next greater/smaller element"**, "span", histograms.

## Core idea
- **Stack:** last in, first out (LIFO). It remembers the most recent unresolved thing.
- **Monotonic stack:** keep the stack sorted (increasing or decreasing). When a new element breaks the order, pop. The **new element is the answer** ("next greater") for everything you pop. O(n) total.

## Templates
```python
# Matching brackets
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for c in s:
        if c in pairs:
            if not st or st.pop() != pairs[c]: return False
        else:
            st.append(c)
    return not st

# Monotonic decreasing stack → next greater element (store INDICES)
def daily_temperatures(t):
    res = [0] * len(t); st = []
    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop(); res[j] = i - j
        st.append(i)
    return res

# Largest rectangle: increasing stack; on pop, height × width
def largest_rectangle(h):
    h = h + [0]; st = []; best = 0
    for i, x in enumerate(h):
        start = i
        while st and st[-1][1] > x:
            idx, height = st.pop()
            best = max(best, height * (i - idx)); start = idx
        st.append((start, x))
    return best
```

## Pitfalls
- Store **indices** in a monotonic stack when you need distances.
- Check `st` isn't empty before calling `pop()` or reading `st[-1]`.
- Add a sentinel (e.g. a trailing 0) to flush whatever is left on the stack at the end.

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Map closing → opening bracket |
| [ ] | [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | In-stack + out-stack; amortized O(1) |
| [ ] | [Baseball Game](https://leetcode.com/problems/baseball-game/) | Simulate |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Min Stack](https://leetcode.com/problems/min-stack/) | Push `(val, current_min)` pairs |
| [ ] | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Pop 2 operands; use `int(a / b)` for truncation |
| [ ] | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Backtracking: open < n, close < open |
| [ ] | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Monotonic decreasing stack |
| [ ] | [Car Fleet](https://leetcode.com/problems/car-fleet/) | Sort by position descending; stack of arrival times |
| [ ] | [Decode String](https://leetcode.com/problems/decode-string/) | Push `(prev_string, count)` on `[` |
| [ ] | [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) | Collide only when the top is > 0 and the new one is < 0 |
| [ ] | [Online Stock Span](https://leetcode.com/problems/online-stock-span/) | Monotonic stack of (price, span) |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Increasing stack, extend start index on pop |
| [ ] | [Basic Calculator](https://leetcode.com/problems/basic-calculator/) | Push (result, sign) on `(` |
| [ ] | [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Histogram per row |
