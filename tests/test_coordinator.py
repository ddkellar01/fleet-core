"""Pytest suite — coordinator pipeline behavior."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.coordinator import Coordinator

STRONG = {"repo": "example/solid", "has_tests": True, "has_readme": True,
          "has_license": True, "ci_green": True}
WEAK = {"repo": "example/weak", "has_tests": False, "has_readme": True,
        "has_license": False, "ci_green": False}
BROKEN = {"repo": "example/broken", "has_tests": True, "has_readme": True,
          "has_license": True, "ci_green": True, "broken": True}


def test_mission_complete_for_strong():
    c = Coordinator(kb_path=":memory:")
    r = c.run_mission("t", candidate=dict(STRONG))
    assert r["status"] == "complete"
    assert set(r["stages"]) == {"scout", "verify", "learn", "test", "deploy"}


def test_mission_stops_at_verify_for_weak():
    c = Coordinator(kb_path=":memory:")
    r = c.run_mission("t", candidate=dict(WEAK))
    assert r["status"].startswith("stopped_at_verify")
    assert "test" not in r["stages"]


def test_mission_stops_at_test_for_broken():
    c = Coordinator(kb_path=":memory:")
    r = c.run_mission("t", candidate=dict(BROKEN))
    assert r["status"] == "stopped_at_test"
    assert "deploy" not in r["stages"]


def test_fleet_status_lists_five_agents():
    c = Coordinator(kb_path=":memory:")
    roles = sorted(a["role"] for a in c.fleet_status())
    assert roles == ["deployer", "learner", "scout", "tester", "verifier"]


def test_lesson_persists_after_mission():
    c = Coordinator(kb_path=":memory:")
    c.run_mission("triage", candidate=dict(WEAK))
    lessons = c.kb.lessons_for("triage")
    assert len(lessons) == 1
    assert "rejected at verification" in lessons[0]