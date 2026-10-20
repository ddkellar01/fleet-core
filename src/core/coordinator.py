"""Coordinator — runs missions through the five-role pipeline.

Pipeline: scout discovers -> verifier challenges -> learner records the
lesson -> tester proves it in the sandbox -> deployer ships it.
A candidate only advances on a verifier 'pass' and a tester pass;
anything else stops the line and the learner's lesson says why.
"""
from __future__ import annotations

from ..agents.deployer import Deployer
from ..agents.learner import Learner
from ..agents.scout import Scout
from ..agents.tester import Tester
from ..agents.verifier import Verifier
from .knowledge_base import KnowledgeBase
from .message_bus import MessageBus


class Coordinator:
    def __init__(self, kb_path: str = "fleet.db"):
        self.bus = MessageBus()
        self.kb = KnowledgeBase(kb_path)
        self.scout = Scout("scout-1", self.bus, self.kb)
        self.verifier = Verifier("verifier-1", self.bus, self.kb)
        self.learner = Learner("learner-1", self.bus, self.kb)
        self.tester = Tester("tester-1", self.bus, self.kb)
        self.deployer = Deployer("deployer-1", self.bus, self.kb)
        self.agents = [self.scout, self.verifier, self.learner,
                       self.tester, self.deployer]

    def fleet_status(self) -> list[dict]:
        return [a.heartbeat() for a in self.agents]

    def run_mission(self, topic: str, candidate: dict | None = None) -> dict:
        report: dict = {"topic": topic, "stages": {}, "status": "running"}

        found = self.scout.run_task({"mission": topic, "topic": topic})
        report["stages"]["scout"] = found
        cand = candidate or (found["candidates"][0] if found.get("candidates") else {})

        verdict = self.verifier.run_task({"mission": topic, "candidate": cand})
        report["stages"]["verify"] = verdict

        lesson = self.learner.run_task({"mission": topic, "pattern": topic,
                                        "outcome": verdict})
        report["stages"]["learn"] = lesson

        if verdict.get("verdict") != "pass":
            report["status"] = f"stopped_at_verify ({verdict.get('verdict')})"
            return report

        tested = self.tester.run_task({"mission": topic, "candidate": cand})
        report["stages"]["test"] = tested
        if not tested.get("passed"):
            report["status"] = "stopped_at_test"
            return report

        deployed = self.deployer.run_task({"mission": topic, "candidate": cand,
                                            "tested": True})
        report["stages"]["deploy"] = deployed
        report["status"] = "complete"
        return report