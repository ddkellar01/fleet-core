"""Scout agent — discovers candidate work for the fleet.

Watches configured sources (repos, issue trackers, feeds) for signals:
failing CI, new releases, unpatched advisories, stale projects worth
reviving. Findings go to the knowledge base for the verifier to challenge.
Simulation candidates by default.
"""
from __future__ import annotations

from .base_agent import BaseAgent

_SIM_CANDIDATES: list[dict] = [
    {"repo": "example/api-gateway", "signal": "failing CI on main",
     "has_tests": True, "has_readme": True, "has_license": True, "ci_green": False},
    {"repo": "example/data-pipeline", "signal": "dependency advisory published",
     "has_tests": True, "has_readme": True, "has_license": False, "ci_green": True},
    {"repo": "example/mobile-client", "signal": "no release in 180 days",
     "has_tests": False, "has_readme": True, "has_license": True, "ci_green": True},
]


class Scout(BaseAgent):
    role = "scout"

    def process(self, task: dict) -> dict:
        topic = task.get("topic", "general")
        limit = int(task.get("limit", 3))
        candidates = [dict(c, topic=topic) for c in _SIM_CANDIDATES[:limit]]
        ids = [self.kb.save_finding(topic, c) for c in candidates]
        return {"topic": topic, "found": len(candidates),
                "finding_ids": ids, "candidates": candidates}