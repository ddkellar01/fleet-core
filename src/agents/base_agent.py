"""Base agent — lifecycle every fleet role inherits.

Handles status, heartbeat, task bookkeeping, publishing results to the
bus, and recording outcomes to the knowledge base. A role only has to
implement process(task) -> result.
"""
from __future__ import annotations

from ..core.knowledge_base import KnowledgeBase
from ..core.message_bus import MessageBus


class BaseAgent:
    role = "base"

    def __init__(self, name: str, bus: MessageBus, kb: KnowledgeBase):
        self.name = name
        self.bus = bus
        self.kb = kb
        self.status = "idle"          # idle | busy | down
        self.tasks_done = 0
        self.last_error = ""

    def heartbeat(self) -> dict:
        return {"name": self.name, "role": self.role,
                "status": self.status, "tasks_done": self.tasks_done}

    def process(self, task: dict) -> dict:
        raise NotImplementedError

    def run_task(self, task: dict) -> dict:
        self.status = "busy"
        try:
            result = self.process(task)
            self.tasks_done += 1
            self.bus.publish(f"results.{self.role}", self.name, result)
            self.kb.record_outcome(task.get("mission", "adhoc"), self.role, result)
            return result
        except Exception as exc:
            self.last_error = str(exc)
            return {"error": str(exc), "role": self.role}
        finally:
            self.status = "idle"