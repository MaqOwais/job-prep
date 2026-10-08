"""
🟡 Parking Lot — the most frequently asked LLD question.

Primer: https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/parking_lot/parking_lot.ipynb

Requirements (clarify first!):
  - Multiple levels; spots of sizes SMALL (motorcycle), COMPACT (car), LARGE (bus)
  - A vehicle parks in the smallest spot that fits it; bus needs 1 LARGE spot (simplified)
  - Issue a ticket on entry; compute fee on exit (pluggable pricing → Strategy pattern)
Patterns: Enum for sizes, abstract Vehicle (inheritance), Strategy for pricing,
          composition (Lot has Levels has Spots). Thread safety: a lock around park/leave.
"""
from __future__ import annotations

import itertools
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum


class SpotSize(IntEnum):
    SMALL = 1
    COMPACT = 2
    LARGE = 3


class Vehicle(ABC):
    def __init__(self, plate: str):
        self.plate = plate

    @property
    @abstractmethod
    def size(self) -> SpotSize: ...


class Motorcycle(Vehicle):
    size = SpotSize.SMALL


class Car(Vehicle):
    size = SpotSize.COMPACT


class Bus(Vehicle):
    size = SpotSize.LARGE


@dataclass
class Spot:
    level: int
    number: int
    size: SpotSize
    vehicle: Vehicle | None = None

    def can_fit(self, v: Vehicle) -> bool:
        return self.vehicle is None and v.size <= self.size


@dataclass
class Level:
    number: int
    spots: list[Spot] = field(default_factory=list)

    def find_spot(self, v: Vehicle) -> Spot | None:
        # smallest fitting spot first
        candidates = [s for s in self.spots if s.can_fit(v)]
        return min(candidates, key=lambda s: s.size, default=None)


@dataclass
class Ticket:
    id: int
    vehicle: Vehicle
    spot: Spot
    entry_hour: float


class PricingStrategy(ABC):
    @abstractmethod
    def fee(self, ticket: Ticket, exit_hour: float) -> float: ...


class HourlyPricing(PricingStrategy):
    RATES = {SpotSize.SMALL: 1.0, SpotSize.COMPACT: 2.5, SpotSize.LARGE: 6.0}

    def fee(self, ticket, exit_hour):
        hours = max(1, int(exit_hour - ticket.entry_hour + 0.999))  # round up, min 1h
        return hours * self.RATES[ticket.spot.size]


class ParkingLot:
    def __init__(self, levels: list[Level], pricing: PricingStrategy):
        self.levels = levels
        self.pricing = pricing
        self.active: dict[int, Ticket] = {}
        self._ids = itertools.count(1)
        self._lock = threading.Lock()

    def park(self, v: Vehicle, now: float) -> Ticket | None:
        with self._lock:
            for level in self.levels:
                spot = level.find_spot(v)
                if spot:
                    spot.vehicle = v
                    t = Ticket(next(self._ids), v, spot, now)
                    self.active[t.id] = t
                    return t
            return None  # full

    def leave(self, ticket_id: int, now: float) -> float:
        with self._lock:
            t = self.active.pop(ticket_id)
            t.spot.vehicle = None
            return self.pricing.fee(t, now)

    def available(self) -> dict[SpotSize, int]:
        out = {s: 0 for s in SpotSize}
        for lvl in self.levels:
            for sp in lvl.spots:
                if sp.vehicle is None:
                    out[sp.size] += 1
        return out


if __name__ == "__main__":
    level = Level(0, [Spot(0, 0, SpotSize.SMALL), Spot(0, 1, SpotSize.COMPACT), Spot(0, 2, SpotSize.LARGE)])
    lot = ParkingLot([level], HourlyPricing())
    t1 = lot.park(Motorcycle("M1"), now=0)
    assert t1.spot.size == SpotSize.SMALL  # smallest fitting
    t2 = lot.park(Car("C1"), now=0)
    assert t2.spot.size == SpotSize.COMPACT
    assert lot.park(Car("C2"), now=0).spot.size == SpotSize.LARGE  # car can use large
    assert lot.park(Bus("B1"), now=0) is None  # full
    assert lot.leave(t2.id, now=2.5) == 3 * 2.5  # 3 hours rounded up
    assert lot.available()[SpotSize.COMPACT] == 1
    print("✅ Parking lot tests passed")
