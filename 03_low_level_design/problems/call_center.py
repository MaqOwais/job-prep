"""
🟡 Call Center — escalation via Chain of Responsibility.

Primer: https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/call_center/call_center.ipynb

Requirements:
  - Employees: Operator → Supervisor → Director (escalation order)
  - An incoming call goes to a free operator; if none, a free supervisor; then director
  - If nobody is free, queue the call; when someone frees up, they take the next queued call
    they are allowed to handle
  - An employee can escalate a call to the next rank
"""
from __future__ import annotations

from collections import deque
from enum import IntEnum


class Rank(IntEnum):
    OPERATOR = 0
    SUPERVISOR = 1
    DIRECTOR = 2


class Call:
    def __init__(self, caller: str, min_rank: Rank = Rank.OPERATOR):
        self.caller = caller
        self.min_rank = min_rank
        self.handler: Employee | None = None


class Employee:
    def __init__(self, name: str, rank: Rank, center: CallCenter):
        self.name, self.rank, self.center = name, rank, center
        self.call: Call | None = None

    @property
    def free(self) -> bool:
        return self.call is None

    def take(self, call: Call) -> None:
        self.call, call.handler = call, self

    def end_call(self) -> None:
        self.call = None
        self.center.on_employee_free(self)

    def escalate(self) -> None:
        call = self.call
        call.min_rank = Rank(min(self.rank + 1, Rank.DIRECTOR))
        self.call = None
        self.center.dispatch(call)
        self.center.on_employee_free(self)


class CallCenter:
    def __init__(self):
        self.staff: dict[Rank, list[Employee]] = {r: [] for r in Rank}
        self.queue: deque[Call] = deque()

    def hire(self, name: str, rank: Rank) -> Employee:
        e = Employee(name, rank, self)
        self.staff[rank].append(e)
        return e

    def dispatch(self, call: Call) -> Employee | None:
        for rank in Rank:  # lowest allowed rank first
            if rank < call.min_rank:
                continue
            for e in self.staff[rank]:
                if e.free:
                    e.take(call)
                    return e
        self.queue.append(call)
        return None

    def on_employee_free(self, e: Employee) -> None:
        for _ in range(len(self.queue)):
            call = self.queue.popleft()
            if e.free and call.min_rank <= e.rank:
                e.take(call)
            else:
                self.queue.append(call)


if __name__ == "__main__":
    cc = CallCenter()
    op = cc.hire("Ann", Rank.OPERATOR)
    sup = cc.hire("Sam", Rank.SUPERVISOR)
    c1, c2, c3 = Call("x"), Call("y"), Call("z")
    assert cc.dispatch(c1) is op
    assert cc.dispatch(c2) is sup  # operator busy → supervisor
    assert cc.dispatch(c3) is None and len(cc.queue) == 1  # queued (no director)
    op.end_call()
    assert c3.handler is op and not cc.queue  # queued call picked up
    op.escalate()  # c3 needs a supervisor+, Sam is busy → queued
    assert len(cc.queue) == 1
    sup.end_call()
    assert c3.handler is sup
    print("✅ Call center tests passed")
