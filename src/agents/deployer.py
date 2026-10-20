"""Deployer agent — ships what survived verification and testing.

Refuses anything untested. Records a rollback point with every deploy
so a bad release is one step back, never a rescue mission.
"""
from __future__ import annotations

from .base_agent import BaseAgent


class Deployer(BaseAgent):
    role = "deployer"

    def process(self, task: dict) -> dict:
        candidate = task.get("candidate", {})
        repo = candidate.get("repo", "unknown")
        if not task.get("tested", False):
            return {"repo": repo, "deployed": False,
                    "detail": "Refused: candidate has not passed testing."}
        return {"repo": repo, "deployed": True,
                "rollback_point": f"pre-deploy snapshot of {repo}",
                "detail": "[sim] Deployed with rollback point recorded."}