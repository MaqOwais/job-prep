# 🧱 Low-Level Design (LLD) / Object-Oriented Design

📖 Primer: [Object-oriented design interview questions with solutions](https://github.com/donnemartin/system-design-primer#object-oriented-design-interview-questions-with-solutions)

LLD rounds ask you to **design classes and their interactions** for a real-world system, and often to code the core of it in 45 minutes.

## 🧭 The 6-step approach
1. **Clarify requirements and scope.** Which features? Single-threaded or concurrent? In-memory or persisted?
2. **Identify the core entities (nouns)** → classes. **Actions (verbs)** → methods.
3. **Define relationships:** is-a (inheritance) vs has-a (composition: prefer this), plus the cardinality.
4. **Draw a quick class diagram** (boxes with fields and methods).
5. **Code the core flow.** Clean names, enums for states, small methods.
6. **Discuss extensibility:** "How would you add X?" Mention the patterns and SOLID principles you used, and thread safety.

## 🧱 SOLID principles
| Principle | One-liner | Smell when it's violated |
|---|---|---|
| **S**ingle responsibility | A class has one reason to change | A "God class" that does everything |
| **O**pen/closed | Open for extension, closed for modification | Adding a vehicle type requires editing an if/else chain |
| **L**iskov substitution | Subclasses must be usable wherever the base class is | `Square(Rectangle)` breaks `set_width` |
| **I**nterface segregation | Many small interfaces beat one fat one | Implementing methods that raise `NotImplementedError` |
| **D**ependency inversion | Depend on abstractions, not concrete classes | `OrderService` directly creates `MySQLDatabase()` |

More patterns: [design_patterns.md](design_patterns.md)

## 🧪 Problems (Easy → Hard), all runnable: `python3 problems/<file>.py`
| Level | Problem | Key concepts | Primer solution |
|---|---|---|---|
| 🟢 | [Hash map](problems/hash_map.py) | Chaining, resizing, hashing | [📖](https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/hash_table/hash_map.ipynb) |
| 🟢 | [LRU cache](problems/lru_cache.py) | Hashmap + doubly linked list, O(1) | [📖](https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/lru_cache/lru_cache.ipynb) |
| 🟡 | [Deck of cards (Blackjack)](problems/deck_of_cards.py) | Inheritance, enums, abstract classes | [📖](https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/deck_of_cards/deck_of_cards.ipynb) |
| 🟡 | [Call center](problems/call_center.py) | Escalation (chain of responsibility), queues | [📖](https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/call_center/call_center.ipynb) |
| 🟡 | [Parking lot](problems/parking_lot.py) | Composition, strategy, enums, the most-asked LLD | [📖](https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/parking_lot/parking_lot.ipynb) |
| 🔴 | [Online chat](problems/online_chat.py) | Users, chats, requests, observer pattern | [📖](https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/online_chat/online_chat.ipynb) |
| 🔴 | [Elevator system](problems/elevator.py) | State machine, scheduling strategy | — |

### More LLD questions to practice
Vending machine (state pattern) · Library management · Movie ticket booking (concurrency on seats) · Splitwise (debt simplification) · Snake & ladder / Tic-tac-toe / Chess · Rate limiter class · Logger (singleton + chain of responsibility) · ATM · Hotel booking · Food delivery (your QEATS project!)

## 🔗 Resources
- [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design): many LLD problems with code
- [Refactoring.Guru: design patterns](https://refactoring.guru/design-patterns): the best visual pattern explanations
- *Head First Design Patterns*
