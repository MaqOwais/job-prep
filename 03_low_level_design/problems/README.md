# 🧪 LLD Problems: Questions & Answers

Code each design first ([back to LLD guide](../README.md)), run it with python3 <file>.py, then test yourself below.

| Problem | Code |
|---|---|
| [LRU cache](#lru-cache) | [lru_cache.py](lru_cache.py) |
| [Hash map](#hash-map) | [hash_map.py](hash_map.py) |
| [Parking lot](#parking-lot) | [parking_lot.py](parking_lot.py) |
| [Deck of cards (Blackjack)](#deck-of-cards-blackjack) | [deck_of_cards.py](deck_of_cards.py) |
| [Call center](#call-center) | [call_center.py](call_center.py) |
| [Online chat](#online-chat) | [online_chat.py](online_chat.py) |
| [Elevator system](#elevator-system) | [elevator.py](elevator.py) |

---

## LRU cache

📄 Code: [lru_cache.py](lru_cache.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why do you need a doubly linked list rather than a singly linked one?</b></summary>

To remove an arbitrary node in **O(1)**, you need its **previous** node to relink the list. A doubly linked list stores prev pointers, so moving a node to the front or evicting the tail is constant time.

</details>

<details>
<summary><b>Q2. What are the sentinel head and tail nodes for?</b></summary>

They remove **edge cases**: the list is never empty and every real node always has non-null prev and next, so insert and remove need no special handling for the first or last element.

</details>

<details>
<summary><b>Q3. How would you make this cache thread-safe?</b></summary>

Wrap get and put in a single **lock**, since both mutate the list (get moves the node to the front). For higher concurrency, use **lock striping / sharding** (N independent LRU segments by key hash), at the cost of only approximate global LRU.

</details>

<details>
<summary><b>Q4. How would you add a per-entry TTL?</b></summary>

Store an expires_at timestamp in each node. On get, treat expired entries as misses and remove them (**lazy expiry**). Optionally run a background sweep, or keep a min-heap ordered by expiry to evict proactively.

</details>

<details>
<summary><b>Q5. How does LFU differ, and how is it implemented in O(1)?</b></summary>

LFU evicts the **least frequently** used key (ties broken by recency). O(1) design: key → node map, plus **frequency → doubly linked list** buckets, plus a min_freq pointer. Each access moves the node to the next frequency bucket.

</details>

---

## Hash map

📄 Code: [hash_map.py](hash_map.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Separate chaining vs open addressing?</b></summary>

**Chaining:** each bucket holds a list of entries. Simple, degrades gracefully, and deletion is easy. **Open addressing:** store entries in the array itself and probe on collisions (linear or quadratic, double hashing). Cache-friendly and no extra pointers, but deletion needs tombstones and performance drops sharply at high load factors.

</details>

<details>
<summary><b>Q2. Why resize when the load factor exceeds about 0.75?</b></summary>

As buckets fill, chains or probe sequences grow and operations drift from O(1) toward O(n). Doubling the capacity and **rehashing** keeps chains short. Since the size doubles, the total rehash cost is spread out, giving **amortized O(1)** inserts.

</details>

<details>
<summary><b>Q3. What is the worst-case complexity, and when does it happen?</b></summary>

**O(n)**, when many keys collide into the same bucket (a poor hash function or adversarial keys, the basis of hash-flooding DoS attacks). Mitigations: good or randomized hashing (Python salts string hashes), and tree-based buckets (Java 8 switches long chains to red-black trees).

</details>

<details>
<summary><b>Q4. Why does the capacity often use a power of two?</b></summary>

Then index = hash & (capacity − 1) replaces the slower modulo. It requires a good hash that mixes the bits well (Java's HashMap mixes the high bits into the low bits). Prime capacities are another approach that is more forgiving of weak hashes.

</details>

<details>
<summary><b>Q5. How would you make the hash map thread-safe?</b></summary>

A global lock (simple, but contended), **lock striping** (a lock per bucket segment, as in Java's old ConcurrentHashMap), or fine-grained CAS on buckets with lock-free reads (modern ConcurrentHashMap). Resizing must be coordinated.

</details>

---

## Parking lot

📄 Code: [parking_lot.py](parking_lot.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Which classes and relationships make up the core design?</b></summary>

ParkingLot **has** Levels, which **have** Spots (composition). **Vehicle** is abstract, with Motorcycle, Car, and Bus subclasses (inheritance). **Ticket** links a vehicle, a spot, and the entry time. **PricingStrategy** is an interface (Strategy pattern). SpotSize is an enum.

</details>

<details>
<summary><b>Q2. How would you add a new vehicle type, like an electric car needing a charging spot?</b></summary>

Add an ElectricCar class and a spot capability (e.g., has_charger or a SpotType enum), and extend the spot-fitting rule. Thanks to Open/Closed, the lot and level logic don't change, only the can_fit rule and the new classes.

</details>

<details>
<summary><b>Q3. How do you prevent two entry gates from assigning the same spot?</b></summary>

Make finding and claiming a spot **atomic**: a lock around park/leave (as in the code), or per-level locks for more concurrency. With a database, use a conditional update on the spot (UPDATE ... WHERE vehicle IS NULL) and check that it succeeded.

</details>

<details>
<summary><b>Q4. How would you support different pricing (hourly, flat weekend, monthly pass)?</b></summary>

Inject a **PricingStrategy** (Strategy pattern). Select it by time or membership via a factory, or compose strategies (e.g., a discount decorator on top of hourly pricing). Fee calculation stays out of ParkingLot.

</details>

<details>
<summary><b>Q5. How do you find a free spot fast in a lot with 10,000 spots?</b></summary>

Keep **free-spot sets or min-heaps per size** (per level), instead of scanning every spot. Park pops a spot and leave pushes it back, both O(log n) or O(1). Also maintain availability counters for the entrance display board.

</details>

---

## Deck of cards (Blackjack)

📄 Code: [deck_of_cards.py](deck_of_cards.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How is the design reusable for games other than Blackjack?</b></summary>

The generic Card, Deck, and Hand classes hold the game-independent logic. Blackjack-specific rules live in the **subclasses** BlackjackCard (value) and BlackjackHand (scoring). A Poker game would add PokerHand without touching the base classes (Open/Closed).

</details>

<details>
<summary><b>Q2. How do you score a Blackjack hand with multiple aces?</b></summary>

Count every ace as **1**, then upgrade one ace to 11 (+10) while the total stays ≤ 21. At most one ace can ever count as 11 without busting.

</details>

<details>
<summary><b>Q3. How would you test shuffle randomness deterministically?</b></summary>

**Inject a seeded RNG** (the Deck takes a seed or a random.Random instance), so tests get reproducible orders. For statistical fairness, shuffle many times and check that position frequencies are uniform. The shuffle itself should be Fisher-Yates (random.shuffle).

</details>

<details>
<summary><b>Q4. How would you support multiple decks (a 6-deck shoe)?</b></summary>

Create a **Shoe** that composes N Deck instances (or N × 52 cards), with a cut card and reshuffle threshold. The rest of the game still calls deal(), and the source of cards is swappable.

</details>

<details>
<summary><b>Q5. Why use an Enum for suits?</b></summary>

Type safety and a fixed set of valid values (no typos like "harts"), easy iteration (for s in Suit), readable comparisons, and IDE support. Ranks could also be an IntEnum.

</details>

---

## Call center

📄 Code: [call_center.py](call_center.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Which design pattern does call escalation use?</b></summary>

**Chain of responsibility**: a call is offered to operators first, then supervisors, then directors. Each level handles the call if it can or passes it up. Escalation sets the call's minimum rank and re-dispatches it.

</details>

<details>
<summary><b>Q2. What happens when every employee is busy?</b></summary>

The call goes into a **FIFO queue**. When an employee frees up, they take the oldest queued call they're allowed to handle (the call's min_rank ≤ their rank). Calls are never dropped.

</details>

<details>
<summary><b>Q3. How would you add call priorities (VIP customers)?</b></summary>

Replace the FIFO queue with a **priority queue** keyed on (priority, arrival_time), so VIPs are served first and arrival order still breaks ties. Add aging to prevent starvation of normal calls.

</details>

<details>
<summary><b>Q4. How would this design change for a real distributed call center?</b></summary>

The queue moves to a **durable message broker or DB**, the employee state to a shared store with atomic assignment (a conditional update so two dispatchers can't assign the same agent), a routing service matches skills, and metrics track wait times and SLAs.

</details>

<details>
<summary><b>Q5. How would you make dispatch thread-safe?</b></summary>

Guard the employee free/busy state and the queue with a **lock** (or a lock per rank), and make "find a free employee and assign" one atomic step, so two concurrent calls can't grab the same employee.

</details>

---

## Online chat

📄 Code: [online_chat.py](online_chat.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Where is the Observer pattern used?</b></summary>

A **Chat** is the subject and its member **Users** are observers. When a message is sent, the chat notifies every other member via on_message. In a real system that callback would push over a WebSocket or enqueue a notification.

</details>

<details>
<summary><b>Q2. Why do PrivateChat and GroupChat share a Chat base class?</b></summary>

Both have members, message history, and send(). The subclasses add their own rules: a private chat **requires friendship** and exactly 2 members; a group chat allows add and remove. That's code reuse plus polymorphism wherever a Chat is expected.

</details>

<details>
<summary><b>Q3. How would you add read receipts?</b></summary>

Track a **last_read_message_id per (user, chat)**. When a user opens the chat, update it and notify the sender (observer). Unread count = messages after last_read. That avoids storing per-message read flags.

</details>

<details>
<summary><b>Q4. How would message ordering work across distributed servers?</b></summary>

Assign message IDs from a **per-chat monotonic sequence** or Snowflake IDs on the server (never client clocks), and order by ID. The LLD's itertools counter per chat models exactly this.

</details>

<details>
<summary><b>Q5. How would you support message editing and deletion?</b></summary>

Make Message mutable through methods (edit(new_text) with edited_at, delete() setting a tombstone flag), keep the edit history if required, and **notify observers** with an update event so clients re-render. Enforce permissions (only the sender, or admins in groups).

</details>

---

## Elevator system

📄 Code: [elevator.py](elevator.py)

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. What is the SCAN (elevator) algorithm?</b></summary>

The car keeps moving in its current direction, serving every requested floor along the way, and **reverses only when there are no more requests ahead**. Like a disk arm. It avoids the starvation and thrashing of nearest-first scheduling.

</details>

<details>
<summary><b>Q2. How does the dispatcher choose which elevator serves a hall call?</b></summary>

A **strategy** computes a cost per car: the distance if the car is idle or already moving toward the floor in the requested direction, and a large penalty if it's moving away. It picks the lowest cost. The strategy is swappable (zoning, energy-saving, peak-hour modes).

</details>

<details>
<summary><b>Q3. Which states does an elevator have, and why model them explicitly?</b></summary>

IDLE, MOVING_UP, MOVING_DOWN (plus DOORS_OPEN, MAINTENANCE, EMERGENCY in a fuller design). An explicit **state machine** makes valid transitions clear, prevents illegal actions (moving with the doors open), and simplifies adding modes. That's the State pattern.

</details>

<details>
<summary><b>Q4. How would you handle capacity limits?</b></summary>

Track the load or passenger count per car. When full, **skip hall calls** (but still stop for car calls to let people off), and let the dispatcher reassign the skipped hall call to another car.

</details>

<details>
<summary><b>Q5. How would you make the system concurrent and safe?</b></summary>

Requests arrive from many buttons at once, so protect each car's stop set with a **lock** (or route all commands through a per-car queue processed by one thread, the actor model). The dispatcher's choose-and-assign step must be atomic.

</details>
