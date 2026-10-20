"""Heartbeat monitor — keeps the fleet honest about who's alive.

Nodes touch the registry on every task. The monitor sweeps on an
interval: a node silent past the timeout is marked stale, past the
hard limit it's down, and the coordinator stops routing work to it.
"""
from __future__ import annotations

import time

from .node_registry import NodeRegistry


class HeartbeatMonitor:
    def __init__(self, registry: NodeRegistry,
                 stale_after_s: float = 30.0, down_after_s: float = 120.0):
        self.registry = registry
        self.stale_after_s = stale_after_s
        self.down_after_s = down_after_s

    def sweep(self, now: float | None = None) -> dict:
        """Reclassify nodes by silence. Returns counts by status."""
        now = now if now is not None else time.time()
        counts = {"online": 0, "stale": 0, "down": 0}
        for node in self.registry._nodes.values():
            silent = now - node.last_seen
            if silent > self.down_after_s:
                node.status = "down"
            elif silent > self.stale_after_s:
                node.status = "stale"
            counts[node.status] += 1
        return counts

    def healthy(self) -> bool:
        counts = self.sweep()
        return counts["down"] == 0