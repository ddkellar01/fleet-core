"""Verifier agent — challenges findings before anyone builds on them.

The Socratic pass: score the evidence behind a candidate, ask the hard
questions out loud, and return a verdict — pass, challenge, or reject.
Nothing reaches the tester without surviving this agent.
"""
from __future__ import annotations

from .base_agent import BaseAgent


class Verifier(BaseAgent):
    role = "verifier"

    CHECKS = ("has_tests", "has_readme", "has_license", "ci_green")

    def process(self, task: dict) -> dict:
        candidate = task.get("candidate", {})
        checks = {c: bool(candidate.get(c, False)) for c in self.CHECKS}
        score = sum(checks.values()) / len(self.CHECKS)
        verdict = "pass" if score >= 0.75 else "challenge" if score >= 0.5 else "reject"
        questions = [f"Why is '{c}' missing on {candidate.get('repo', 'unknown')}?"
                     for c, ok in checks.items() if not ok]
        return {"repo": candidate.get("repo", "unknown"), "verdict": verdict,
                "score": score, "checks": checks, "questions": questions}