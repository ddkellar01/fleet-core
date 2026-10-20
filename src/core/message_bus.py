"""In-memory message bus — how fleet agents talk.

Agents publish results to topics (results.scout, results.tester, ...);
any other agent or the coordinator can subscribe. Every message is kept
in history so missions can be audited and replayed.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable


@dataclass
class Message:
    topic: str
    sender: str
    payload: dict
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MessageBus:
    def __init__(self):
        self._subs: dict[str, list[Callable[[Message], None]]] = defaultdict(list)
        self.history: list[Message] = []

    def subscribe(self, topic: str, handler: Callable[[Message], None]) -> None:
        self._subs[topic].append(handler)

    def publish(self, topic: str, sender: str, payload: dict) -> Message:
        msg = Message(topic=topic, sender=sender, payload=payload)
        self.history.append(msg)
        for handler in self._subs.get(topic, []):
            handler(msg)
        return msg

    def history_for(self, topic: str) -> list[Message]:
        return [m for m in self.history if m.topic == topic]