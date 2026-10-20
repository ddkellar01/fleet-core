"""Tester agent — proves candidates in a sandbox before deployment.

Runs a candidate's checks in isolation and reports pass/fail with the
failing tests named. Simulation results by default; bench mode wires
this to the Docker sandbox runner.
"""
from __future__ import annotations

from .base_agent import BaseAgent


class Tester(BaseAgent):
    role = "tester"

    def process(self, task: dict) -> dict:
        candidate = task.get("candidate", {})
        repo = candidate.get("repo", "unknown")
        broken = bool(candidate.get("broken", False))
        tests_run = 24
        failures = ["tests/test_api.py::test_timeout"] if broken else []
        return {"repo": repo, "sandbox": "docker",
                "tests_run": tests_run, "passed": not broken,
                "failures": failures}