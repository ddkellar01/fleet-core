"""Load balancer — routes tasks to the least-loaded healthy node of a role.

Sits between the coordinator and the node registry: route() picks a
node and reserves a slot, release() frees it. Down nodes (per the
heartbeat monitor) never receive work.
"""
from __future__ import annotations

from .heartbeat import HeartbeatMonitor
from .node_registry import Node, NodeRegistry


class LoadBalancer:
    def __init__(self, registry: NodeRegistry, monitor: HeartbeatMonitor):
        self.registry = registry
        self.monitor = monitor

    def route(self, role: str) -> Node | None:
        self.monitor.sweep()                    # refresh health first
        node = self.registry.pick(role)
        if node:
            node.active += 1
            self.registry.touch(node.name)
        return node

    def release(self, node: Node) -> None:
        if node.active > 0:
            node.active -= 1
        self.registry.touch(node.name)

    def distribution(self) -> dict:
        dist: dict[str, int] = {}
        for n in self.registry.list_nodes():
            dist[n["role"]] = dist.get(n["role"], 0) + n["active"]
        return dist