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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What is a monotonic stack, and what problems does it solve?</b></summary>

A stack kept in increasing or decreasing order. When a new element breaks the order, you pop, and the new element is the **next greater (or smaller) element** for everything popped. It solves next-greater-element, daily temperatures, stock span, and histogram areas in **O(n)**.

</details>

<details>
<summary><b>Q2. Why store indices instead of values in a monotonic stack?</b></summary>

Indices give you both the **value** (array lookup) and the **distance or width** (i − j), which you need for "days until warmer" or rectangle widths.

</details>

<details>
<summary><b>Q3. How do you implement Min Stack with O(1) getMin?</b></summary>

Push pairs **(value, min so far)**, or keep a second stack of minimums. getMin reads the top's stored minimum. Popping restores the previous minimum automatically.

</details>

<details>
<summary><b>Q4. Explain Largest Rectangle in Histogram.</b></summary>

Keep an **increasing stack** of (start_index, height). When a lower bar arrives, pop the taller bars. Each popped bar's rectangle extends from its start to the current index (area = height × width), and the new bar inherits the earliest start popped. Add a trailing 0 to flush the stack. O(n).

</details>

<details>
<summary><b>Q5. How do you implement a queue using two stacks with amortized O(1) operations?</b></summary>

Push onto an **in** stack. For pop or peek, if the **out** stack is empty, move everything from in to out (reversing the order), then pop from out. Each element moves at most once, so the cost is amortized O(1).

</details>
