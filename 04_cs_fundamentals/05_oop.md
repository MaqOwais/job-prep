# 5. Object-Oriented Programming

📖 Related: [LLD approach + SOLID](../03_low_level_design/README.md) · [Design patterns](../03_low_level_design/design_patterns.md)

## The 4 pillars
| Pillar | Meaning | Python example |
|---|---|---|
| **Encapsulation** | Bundle data + behavior; hide internal state | `_balance` + `deposit()` instead of a public field |
| **Abstraction** | Expose *what*, hide *how* | `abc.ABC` with `@abstractmethod` |
| **Inheritance** | "is-a": reuse and specialize | `class Car(Vehicle)` |
| **Polymorphism** | One interface, many implementations | `shape.area()` works for Circle and Square |

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def __init__(self, r): self._r = r            # encapsulated
    def area(self): return math.pi * self._r ** 2

class Square(Shape):
    def __init__(self, s): self._s = s
    def area(self): return self._s ** 2

shapes: list[Shape] = [Circle(1), Square(2)]
total = sum(s.area() for s in shapes)            # polymorphism
```

## Key comparisons
- **Composition vs inheritance:** prefer composition ("has-a"). Inheritance couples you to the parent class's implementation (the fragile base class problem).
- **Abstract class vs interface:** an abstract class can hold state and partial implementations. An interface is a pure contract. Python uses ABCs or `typing.Protocol` (duck typing).
- **Overloading** (same name, different parameters: compile time; not native in Python) vs **overriding** (a subclass redefines a method: runtime).
- **Static vs instance vs class methods** (`@staticmethod`, `@classmethod`).
- **Shallow vs deep copy.**
- **`__eq__` and `__hash__`:** objects used as dict keys must have consistent equality and hashing.
- **Dunder methods:** `__init__`, `__repr__`, `__eq__`, `__lt__` (sorting), `__len__`, `__iter__`, `__enter__`/`__exit__` (context managers).
- **MRO / the diamond problem:** Python uses C3 linearization (`Class.__mro__`).

## SOLID (one-liners)
S: one reason to change · O: extend, don't modify · L: subtypes must be substitutable · I: small interfaces · D: depend on abstractions. Examples in [LLD README](../03_low_level_design/README.md#-solid-principles).

## Clean code and testing (SWE rounds also check these)
- Meaningful names, small functions, no magic numbers, guard clauses, DRY (but avoid premature abstraction).
- **Testing pyramid:** many unit tests → fewer integration tests → few end-to-end tests. Mocks and stubs. TDD (red → green → refactor).
- Code review etiquette: be specific, kind, and explain the reasoning.

## Interview questions
1. Explain the 4 pillars with a real example from your own code (e.g., QEATS services, the Jukebox design).
2. Composition vs inheritance: when would you use each?
3. What is the Liskov substitution principle? Give a violation.
4. Abstract class vs interface.
5. How does Python handle multiple inheritance?
