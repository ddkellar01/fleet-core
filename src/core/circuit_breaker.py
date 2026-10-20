"""Circuit breaker — isolates a failing agent before it poisons missions.

Wraps agent calls: after N consecutive failures the breaker opens and
calls fail fast for a cooldown; then one trial call decides whether
the agent is back. Inspired by IvyTech's swarm_core circuit breaker.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class CircuitBreaker:
    name: str
    failure_threshold: int = 3
    cooldown_s: float = 60.0
    failures: int = 0
    state: str = "closed"             # closed | open | half_open
    opened_at: float = 0.0
    _clock: Callable[[], float] = field(default=time.time, repr=False)

    def allow(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open" and self._clock() - self.opened_at >= self.cooldown_s:
            self.state = "half_open"
            return True
        return False

    def record_success(self) -> None:
        self.failures = 0
        self.state = "closed"

    def record_failure(self) -> None:
        self.failures += 1
        if self.state == "half_open" or self.failures >= self.failure_threshold:
            self.state = "open"
            self.opened_at = self._clock()

    def call(self, fn: Callable[[], dict]) -> dict:
        if not self.allow():
            return {"error": f"circuit open for {self.name}", "breaker": "open"}
        try:
            result = fn()
            if isinstance(result, dict) and "error" in result:
                self.record_failure()
            else:
                self.record_success()
            return result
        except Exception as exc:
            self.record_failure()
            return {"error": str(exc), "breaker": self.state}