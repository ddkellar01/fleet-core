"""Pytest suite — the five agent roles, each in isolation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agents.deployer import Deployer
from src.agents.learner import Learner
from src.agents.scout import Scout
from src.agents.tester import Tester
from src.agents.verifier import Verifier
from src.core.knowledge_base import KnowledgeBase
from src.core.message_bus import MessageBus


def make(role_cls):
    bus, kb = MessageBus(), KnowledgeBase(":memory:")
    return role_cls("agent-1", bus, kb), bus, kb


def test_scout_finds_and_records():
    scout, bus, kb = make(Scout)
    out = scout.run_task({"topic": "x"})
    assert out["found"] == 3
    assert len(kb.recent_findings()) == 3
    assert len(bus.history_for("results.scout")) == 1


def test_verifier_verdicts():
    v, _, _ = make(Verifier)
    full = {"repo": "a", "has_tests": 1, "has_readme": 1,
            "has_license": 1, "ci_green": 1}
    assert v.process({"candidate": full})["verdict"] == "pass"
    half = {"repo": "b", "has_tests": 1, "has_readme": 1}
    r = v.process({"candidate": half})
    assert r["verdict"] == "challenge" and len(r["questions"]) == 2
    none = {"repo": "c"}
    assert v.process({"candidate": none})["verdict"] == "reject"


def test_learner_saves_lesson():
    learner, _, kb = make(Learner)
    out = learner.run_task({"pattern": "p",
                            "outcome": {"verdict": "challenge", "repo": "z",
                                        "questions": ["q1"]}})
    assert "challenged" in out["lesson"]
    assert kb.lessons_for("p") == [out["lesson"]]


def test_tester_pass_and_fail():
    t, _, _ = make(Tester)
    assert t.process({"candidate": {"repo": "a"}})["passed"]
    bad = t.process({"candidate": {"repo": "a", "broken": True}})
    assert not bad["passed"] and bad["failures"]


def test_deployer_refuses_untested():
    d, _, _ = make(Deployer)
    assert d.process({"candidate": {"repo": "a"}})["deployed"] is False
    ok = d.process({"candidate": {"repo": "a"}, "tested": True})
    assert ok["deployed"] and "rollback" in ok["rollback_point"]