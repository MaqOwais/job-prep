"""
🔴 Elevator System — state machine + pluggable scheduling (Strategy).

Requirements (clarify!):
  - N elevators, floors 0..F-1
  - Hall calls (floor + direction) and car calls (button inside the car)
  - Each elevator: state IDLE / MOVING_UP / MOVING_DOWN; serves stops in its current direction
    first (SCAN / "elevator algorithm"), then reverses
  - Dispatcher picks an elevator for each hall call (Strategy: nearest suitable elevator)
  - Simulation via step(): each step moves every elevator one floor
Follow-ups: capacity/weight, door state, emergency mode, peak-hour zoning, concurrency (lock per car).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class Elevator:
    def __init__(self, eid: int, floor: int = 0):
        self.id, self.floor = eid, floor
        self.direction = Direction.IDLE
        self.stops: set[int] = set()
        self.log: list[int] = []  # floors where the doors opened

    def add_stop(self, floor: int) -> None:
        if floor != self.floor or self.direction != Direction.IDLE:
            self.stops.add(floor)
        else:
            self.log.append(floor)  # already here → open doors

    def step(self) -> None:
        if not self.stops:
            self.direction = Direction.IDLE
            return
        if self.direction == Direction.IDLE:
            nearest = min(self.stops, key=lambda f: abs(f - self.floor))
            self.direction = Direction.UP if nearest > self.floor else Direction.DOWN
        ahead = [f for f in self.stops if (f - self.floor) * self.direction.value > 0]
        if not ahead and self.floor not in self.stops:  # nothing ahead → reverse (SCAN)
            self.direction = Direction.UP if self.direction == Direction.DOWN else Direction.DOWN
        if self.floor not in self.stops:
            self.floor += self.direction.value
        if self.floor in self.stops:
            self.stops.discard(self.floor)
            self.log.append(self.floor)
            if not self.stops:
                self.direction = Direction.IDLE


class DispatchStrategy(ABC):
    @abstractmethod
    def choose(self, elevators: list[Elevator], floor: int, direction: Direction) -> Elevator: ...


class NearestSuitable(DispatchStrategy):
    """Prefer idle cars or cars already moving toward the floor in the same direction."""

    def choose(self, elevators, floor, direction):
        def cost(e: Elevator) -> int:
            dist = abs(e.floor - floor)
            if e.direction == Direction.IDLE:
                return dist
            moving_toward = (floor - e.floor) * e.direction.value >= 0
            if moving_toward and e.direction == direction:
                return dist
            return dist + 100  # penalize cars going the other way

        return min(elevators, key=cost)


class ElevatorSystem:
    def __init__(self, n: int, floors: int, strategy: DispatchStrategy | None = None):
        self.floors = floors
        self.elevators = [Elevator(i) for i in range(n)]
        self.strategy = strategy or NearestSuitable()

    def hall_call(self, floor: int, direction: Direction) -> Elevator:
        assert 0 <= floor < self.floors
        e = self.strategy.choose(self.elevators, floor, direction)
        e.add_stop(floor)
        return e

    def car_call(self, eid: int, floor: int) -> None:
        self.elevators[eid].add_stop(floor)

    def step(self, times: int = 1) -> None:
        for _ in range(times):
            for e in self.elevators:
                e.step()


if __name__ == "__main__":
    sys_ = ElevatorSystem(n=2, floors=10)
    sys_.elevators[1].floor = 9
    e = sys_.hall_call(8, Direction.DOWN)
    assert e.id == 1  # nearest
    e0 = sys_.hall_call(2, Direction.UP)
    assert e0.id == 0
    sys_.step(2)
    assert sys_.elevators[0].floor == 2 and sys_.elevators[1].floor == 8
    sys_.car_call(0, 7)
    sys_.car_call(0, 4)
    sys_.step(5)
    assert sys_.elevators[0].log == [2, 4, 7]  # SCAN order upward
    print("✅ Elevator tests passed")
