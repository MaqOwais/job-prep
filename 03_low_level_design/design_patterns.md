# Design Patterns Cheat Sheet (the ones that come up in interviews)

📖 Visual explanations: [Refactoring.Guru](https://refactoring.guru/design-patterns/catalog)

## Creational
| Pattern | Use when | Interview example |
|---|---|---|
| **Singleton** | Exactly one instance (config, logger, connection pool) | Parking lot instance, Logger |
| **Factory** | Create objects without the caller knowing the concrete class | `VehicleFactory.create("car")` |
| **Builder** | Many optional constructor parameters | Building an HTTP request, a pizza order |

```python
class Logger:                         # Singleton (simple, not thread-safe)
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Structural
| Pattern | Use when | Example |
|---|---|---|
| **Adapter** | Make an incompatible interface fit | Wrap a 3rd-party payment SDK behind your `PaymentGateway` interface |
| **Decorator** | Add behavior without subclassing | Add toppings to a coffee; Python `@decorators` for logging/caching |
| **Facade** | A simple front for a complex subsystem | `OrderFacade.place_order()` hides inventory + payment + shipping |
| **Proxy** | Control access (lazy loading, caching, auth) | A caching proxy in front of a slow service |
| **Composite** | Tree of objects treated uniformly | File system (files and folders) |

## Behavioral
| Pattern | Use when | Example |
|---|---|---|
| **Strategy** | Swap algorithms at runtime | Pricing strategy, elevator scheduling, parking fee calculation |
| **Observer** | Notify many listeners of changes | Chat notifications, stock price subscribers, event bus |
| **State** | Behavior depends on internal state | Vending machine, order lifecycle, elevator |
| **Command** | Encapsulate a request (undo/redo, queues) | Text editor undo, remote control |
| **Chain of responsibility** | Pass a request along handlers until one handles it | Call center escalation, logging levels, middleware |
| **Iterator** | Traverse without exposing internals | Python generators |
| **Template method** | Algorithm skeleton with overridable steps | A game loop, data pipeline steps |

```python
from abc import ABC, abstractmethod
class PricingStrategy(ABC):                 # Strategy
    @abstractmethod
    def price(self, hours: float) -> float: ...
class HourlyPricing(PricingStrategy):
    def price(self, hours): return 5 * hours
class FlatPricing(PricingStrategy):
    def price(self, hours): return 20
class Ticket:
    def __init__(self, strategy: PricingStrategy): self.strategy = strategy
    def fee(self, hours): return self.strategy.price(hours)

class Subject:                              # Observer
    def __init__(self): self._observers = []
    def subscribe(self, fn): self._observers.append(fn)
    def notify(self, event):
        for fn in self._observers: fn(event)
```

## Which pattern for which LLD problem?
| Problem | Patterns |
|---|---|
| Parking lot | Singleton, Strategy (fees), Factory (vehicles) |
| Vending machine | **State** |
| Elevator | State, Strategy (scheduling), Observer (displays) |
| Chat / notifications | **Observer**, Mediator |
| Call center | **Chain of responsibility** |
| Text editor | **Command** (undo/redo), Memento |
| Payment integration | **Adapter**, Strategy |
| Logger | Singleton, Chain of responsibility |

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Strategy vs State pattern: they look similar. What's the difference?</b></summary>

Both delegate behavior to interchangeable objects. **Strategy:** the **client chooses** an algorithm (pricing, sorting, routing), and the strategies don't know each other. **State:** the object's behavior changes with its **internal state**, and states typically **trigger transitions** to other states (vending machine: Idle → HasMoney → Dispensing).

</details>

<details>
<summary><b>Q2. When would you use the Observer pattern? What are its pitfalls?</b></summary>

When many components must react to changes in one subject without tight coupling: UI updates, event buses, notifications, chat delivery. Pitfalls: memory leaks if observers aren't unsubscribed, unexpected update cascades, ordering assumptions, and slow observers blocking the subject (use async dispatch).

</details>

<details>
<summary><b>Q3. How do you make a Singleton thread-safe, and why is it often discouraged?</b></summary>

Use eager initialization, a module-level instance (Python), or **double-checked locking** for lazy initialization. It's discouraged because it's **global mutable state**: it hides dependencies, makes tests hard (shared state between tests), and complicates concurrency. Prefer dependency injection of a single instance.

</details>

<details>
<summary><b>Q4. Factory vs Builder: when do you use each?</b></summary>

A **Factory** decides **which concrete class** to instantiate based on input (VehicleFactory.create("car")). A **Builder** constructs **one complex object step by step** with many optional parameters (HttpRequest.builder().url(..).header(..).timeout(..).build()). It avoids huge constructors.

</details>

<details>
<summary><b>Q5. Which pattern fits undo/redo in a text editor, and how does it work?</b></summary>

**Command**: each edit is an object with execute() and undo(). Executed commands go onto an **undo stack**. Undo pops one, calls undo(), and pushes it onto the **redo stack**. A new command clears the redo stack. Memento can store snapshots for complex state.

</details>
