# 17. Math, Matrix & Bit Manipulation

**Signals:** "without using + or −", "appears once/twice", "power of two", count bits, rotate/spiral a matrix, digits of a number, overflow.

## Bit tricks
| Trick | Meaning |
|---|---|
| `x & 1` | Is x odd? |
| `x & (x - 1)` | Clear the lowest set bit; equals 0 iff x is a power of 2 (for x > 0) |
| `x & -x` | Isolate the lowest set bit |
| `a ^ a = 0`, `a ^ 0 = a` | XOR cancels pairs → find the single number |
| `x >> 1`, `x << 1` | Divide / multiply by 2 |
| `(x >> i) & 1` | i-th bit |
| `bin(x).count('1')` | Popcount (Python) |

Python ints are unbounded. For 32-bit problems, mask with `0xFFFFFFFF`.

## Matrix templates
```python
# Rotate 90° clockwise in place = transpose + reverse each row
def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    for row in m: row.reverse()

# Spiral order with shrinking boundaries
def spiral(m):
    res = []; top, bot, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    while top <= bot and left <= right:
        res += m[top][left:right + 1]; top += 1
        for r in range(top, bot + 1): res.append(m[r][right])
        right -= 1
        if top <= bot: res += m[bot][left:right + 1][::-1]; bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1): res.append(m[r][left])
            left += 1
    return res

# Fast power
def my_pow(x, n):
    if n < 0: x, n = 1 / x, -n
    res = 1
    while n:
        if n & 1: res *= x
        x *= x; n >>= 1
    return res
```

## Problems
### 🟢 Easy
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Single Number](https://leetcode.com/problems/single-number/) | XOR everything |
| [ ] | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | `x &= x − 1` until 0 |
| [ ] | [Counting Bits](https://leetcode.com/problems/counting-bits/) | `dp[i] = dp[i >> 1] + (i & 1)` |
| [ ] | [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | Shift 32 times |
| [ ] | [Missing Number](https://leetcode.com/problems/missing-number/) | XOR of indices and values, or n(n+1)/2 − sum |
| [ ] | [Happy Number](https://leetcode.com/problems/happy-number/) | Cycle detection (set or Floyd) |
| [ ] | [Plus One](https://leetcode.com/problems/plus-one/) | Carry from the back |

### 🟡 Medium
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Rotate Image](https://leetcode.com/problems/rotate-image/) | Transpose + reverse |
| [ ] | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Shrinking boundaries |
| [ ] | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Use the first row/column as markers |
| [ ] | [Pow(x, n)](https://leetcode.com/problems/powx-n/) | Fast exponentiation |
| [ ] | [Multiply Strings](https://leetcode.com/problems/multiply-strings/) | `res[i+j+1] += d1*d2` |
| [ ] | [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) | XOR = sum without carry, AND<<1 = carry; mask to 32 bits |
| [ ] | [Reverse Integer](https://leetcode.com/problems/reverse-integer/) | Check 32-bit overflow |

### 🔴 Hard
| ✓ | Problem | Hint |
|---|---|---|
| [ ] | [Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) | For each point, slopes as a reduced (dy, dx) via gcd |
