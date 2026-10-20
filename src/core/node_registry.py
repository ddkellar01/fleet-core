"""Node registry — who is in the fleet, doing what, with what capacity.

Agents register on startup with a role and a capacity (max concurrent
tasks). The coordinator asks the registry for the least-loaded node of a
role instead of hardcoding agent instances.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    role: str
    capacity: int = 1
    active: int = 0
    status: str = "online"          # online | stale | down
    last_seen: float = field(default_factory=time.time)

    def heartbeat(self) -> dict:
        return {"name": self.name, "role": self.role, "status": self.status,
                "active": self.active, "capacity": self.capacity}


class NodeRegistry:
    def __init__(self):
        self._nodes: dict[str, Node] = {}

    def register(self, name: str, role: str, capacity: int = 1) -> Node:
        node = Node(name=name, role=role, capacity=capacity)
        self._nodes[name] = node
        return node

    def deregister(self, name: str) -> None:
        self._nodes.pop(name, None)

    def touch(self, name: str) -> None:
        node = self._nodes.get(name)
        if node:
            node.last_seen = time.time()
            if node.status == "stale":
                node.status = "online"

    def pick(self, role: str) -> Node | None:
        """Least-loaded online node for a role, or None."""
        candidates = [n for n in self._nodes.values()
                      if n.role == role and n.status == "online"
                      and n.active < n.capacity]
        if not candidates:
            return None
        return min(candidates, key=lambda n: n.active)

    def list_nodes(self) -> list[dict]:
        return [n.heartbeat() for n in self._nodes.values()]

    def get(self, name: str) -> Node | None:
        return self._nodes.get(name)